"""
workflow.py

Defines the LangGraph workflow for parsing a T-Mobile bill. The workflow handles:
- Loading cached parsed bills
- Extracting bill data using an LLM
- Validating extracted data
- Retrying extraction up to 3 times
- Routing to human review when needed
- Uploading approved bills to DynamoDB

Each step is implemented as a LangGraph node operating on an AgentState object.
"""

from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional, Dict, Any

from nodes.increment_retry_node import increment_retry
from nodes.bill_extraction_node import get_bill_info
from nodes.human_review_node import human_review, review_condition
from nodes.upload_node import upload_to_dynamodb
from nodes.save_json_node import save_parsed_bill
from nodes.load_cached_node import load_cached_bill
from nodes.validate_bill_node import validate_bill
from state import AgentState


def validation_route(state: AgentState) -> str:
    """
    Determine the next step after validating the extracted bill.

    Routing logic:
        - If validation_flag is True → bill is valid
        - If invalid and retry_count < 3 → retry extraction
        - If invalid and retries exhausted → escalate to human review

    Args:
        state (AgentState): Current workflow state.

    Returns:
        str: One of:
            "valid"
            "retry_as_invalid"
            "give_up_done_with_retries"
    """
    flag = state["parsed_bill"].get("validation_flag", False)
    retries = state.get("retry_count", 0)

    if flag:
        return "valid"

    if retries < 3:
        return "retry_as_invalid"

    return "give_up_done_with_retries"


def route_after_cache(state: AgentState) -> str:
    """
    Determine whether to skip LLM extraction based on cached data.

    If load_cached_bill populated parsed_bill, we skip extraction entirely.

    Args:
        state (AgentState): Current workflow state.

    Returns:
        str: Either:
            "cached"   – parsed bill already exists
            "no_cache" – no cached bill found
    """
    if state.get("parsed_bill"):
        return "cached"
    return "no_cache"


def build_workflow():
    """
    Build and compile the LangGraph workflow for T-Mobile bill parsing.

    Workflow structure:

        load_cached_bill
            ├── cached → human_review
            └── no_cache → get_bill_info → validate_bill
                                ├── valid → save_parsed_bill → human_review
                                ├── retry_as_invalid → increment_retry → get_bill_info
                                └── give_up_done_with_retries → human_review

        human_review
            ├── approved → upload_to_dynamodb → END
            └── denied → END

    Returns:
        Compiled workflow object.
    """
    workflow = StateGraph(AgentState)

    # Register workflow nodes
    workflow.add_node("load_cached_bill", load_cached_bill)
    workflow.add_node("increment_retry", increment_retry)
    workflow.add_node("get_bill_info", get_bill_info)
    workflow.add_node("validate_bill", validate_bill)
    workflow.add_node("save_parsed_bill", save_parsed_bill)
    workflow.add_node("human_review", human_review)
    workflow.add_node("upload_to_dynamodb", upload_to_dynamodb)

    # Entry point: always attempt to load cached bill first
    workflow.set_entry_point("load_cached_bill")

    # Branch based on cache hit/miss
    workflow.add_conditional_edges(
        "load_cached_bill",
        route_after_cache,
        {
            "cached": "human_review",     # Skip extraction
            "no_cache": "get_bill_info",  # Run extraction
        }
    )

    # Extraction → validation
    workflow.add_edge("get_bill_info", "validate_bill")

    # Validation routing
    workflow.add_conditional_edges(
        "validate_bill",
        validation_route,
        {
            "valid": "save_parsed_bill",
            "retry_as_invalid": "increment_retry",
            "give_up_done_with_retries": "human_review",
        }
    )

    # Retry loop
    workflow.add_edge("increment_retry", "get_bill_info")

    # Save → human review
    workflow.add_edge("save_parsed_bill", "human_review")

    # Human review routing
    workflow.add_conditional_edges(
        "human_review",
        review_condition,
        {
            "approved": "upload_to_dynamodb",
            "denied": END,
        }
    )

    # Upload → end
    workflow.add_edge("upload_to_dynamodb", END)

    return workflow.compile()