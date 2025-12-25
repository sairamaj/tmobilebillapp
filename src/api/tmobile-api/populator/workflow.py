from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional, Dict, Any

from nodes.bill_extraction_node import get_bill_info
from nodes.human_review_node import human_review, review_condition
from nodes.upload_node import upload_to_dynamodb

class AgentState(TypedDict):
    raw_bill_text: Optional[str]
    parsed_bill: Optional[Dict[str, Any]]
    human_feedback: Optional[str]
    upload_status: Optional[str]

def build_workflow():
    workflow = StateGraph(AgentState)

    workflow.add_node("get_bill_info", get_bill_info)
    workflow.add_node("human_review", human_review)
    workflow.add_node("upload_to_dynamodb", upload_to_dynamodb)

    workflow.set_entry_point("get_bill_info")

    workflow.add_edge("get_bill_info", "human_review")

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