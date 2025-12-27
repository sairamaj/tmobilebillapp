from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional, Dict, Any

from nodes.increment_retry_node import increment_retry
from nodes.bill_extraction_node import get_bill_info
from nodes.human_review_node import human_review, review_condition
from nodes.upload_node import upload_to_dynamodb
from nodes.save_json_node import save_parsed_bill
from nodes.load_cached_node import load_cached_bill
from nodes.validate_bill_node import validate_bill_node
from state import AgentState

def validation_route(state: AgentState) -> str:
    flag = state["parsed_bill"].get("validation_flag", False)
    retries = state.get("retry_count", 0)

    if flag:
        return "valid"

    if retries < 3:
        return "retry"

    return "give_up"

def route_after_cache(state: AgentState) -> str:
    """
    If load_cached_bill populated parsed_bill, skip LLM extraction.
    Otherwise, run get_bill_info.
    """
    if state.get("parsed_bill"):
        return "cached"
    return "no_cache"

def build_workflow():
    workflow = StateGraph(AgentState)

    # Nodes
    workflow.add_node("load_cached_bill", load_cached_bill)
    workflow.add_node("increment_retry", increment_retry)   
    workflow.add_node("get_bill_info", get_bill_info)
    workflow.add_node("validate_bill_node", validate_bill_node)   
    workflow.add_node("save_parsed_bill", save_parsed_bill)
    workflow.add_node("human_review", human_review)
    workflow.add_node("upload_to_dynamodb", upload_to_dynamodb)

    # Entry point is ALWAYS load_cached_bill
    workflow.set_entry_point("load_cached_bill")

    # After loading cache, branch based on whether parsed_bill exists
    workflow.add_conditional_edges(
        "load_cached_bill",
        route_after_cache,
        {
            "cached": "human_review",       # cache hit → skip LLM
            "no_cache": "get_bill_info",    # cache miss → extract
        }
    )

    # Normal extraction path
    workflow.add_edge("get_bill_info", "validate_bill_node")      
    workflow.add_conditional_edges(
    "validate_bill_node",
    validation_route,
    {
        "valid": "save_parsed_bill",
        "retry": "increment_retry",
        "give_up": "human_review",
    })

    workflow.add_edge("increment_retry", "get_bill_info")
    workflow.add_edge("save_parsed_bill", "human_review")

    # Human review → upload or end
    workflow.add_conditional_edges(
        "human_review",
        review_condition,
        {
            "approved": "upload_to_dynamodb",
            "denied": END
        }
    )

    workflow.add_edge("upload_to_dynamodb", END)

    return workflow.compile()