from typing import Dict, Any
from viewer import print_bill_table
from services.storage_service import save_temp_bill

def human_review(state: Dict[str, Any]) -> Dict[str, Any]:
    print("\n--- HUMAN REVIEW REQUIRED ---")
    print_bill_table(state.get("parsed_bill", {}))
    feedback = input("Enter 'approve' to continue or anything else to deny: ").strip().lower()
    return {**state, "human_feedback": feedback}

def review_condition(state: Dict[str, Any]):
    return "approved" if state["human_feedback"] == "approve" else "denied"