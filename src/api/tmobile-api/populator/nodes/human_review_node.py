from typing import Dict, Any
from viewer import print_bill_table, print_validation_result
from services.storage_service import save_temp_bill
import json
import os

def human_review(state: Dict[str, Any]) -> Dict[str, Any]:
    print("\n--- HUMAN REVIEW REQUIRED ---")
    print_bill_table(state.get("parsed_bill", {}))
    print_validation_result(state.get("parsed_bill", {}))
    os.makedirs(r"c:\temp", exist_ok=True)
    try:
        with open(r"c:\temp\state.json", "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Failed to write state file: {e}")
    feedback = input("Enter 'approve' to continue or anything else to deny: ").strip().lower()
    return {**state, "human_feedback": feedback}

def review_condition(state: Dict[str, Any]):
    return "approved" if state["human_feedback"] == "approve" else "denied"