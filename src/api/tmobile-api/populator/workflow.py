from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional, Dict, Any

from nodes.bill_extraction_node import get_bill_info
from nodes.human_review_node import human_review, review_condition
from nodes.upload_node import upload_to_dynamodb
from nodes.save_json_node import save_parsed_bill
from nodes.load_cached_node import load_cached_bill


class AgentState(TypedDict):
    pdf_file_name: Optional[str]
    raw_bill_text: Optional[str]
    parsed_bill: Optional[Dict[str, Any]]
    human_feedback: Optional[str]
    upload_status: Optional[str]


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
    workflow.add_node("get_bill_info", get_bill_info)
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
    workflow.add_edge("get_bill_info", "save_parsed_bill")
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