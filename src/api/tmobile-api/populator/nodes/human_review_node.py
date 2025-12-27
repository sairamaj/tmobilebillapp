from typing import Dict, Any
from viewer import print_bill_table, print_validation_result
from services.storage_service import save_temp_bill
import json
import os

def human_review(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Prompt the user for a manual review of the current pipeline state and record their feedback.

    Parameters
    ----------
    state : Dict[str, Any]
        The current pipeline state. This function expects that state may contain a
        "parsed_bill" key (any structure) which will be displayed via
        print_bill_table and print_validation_result.

    Returns
    -------
    Dict[str, Any]
        A copy of the input state merged with a new "human_feedback" key whose value
        is the user's response from stdin, lowercased and stripped. Typical values:
        - "approve" to indicate acceptance
        - any other string to indicate denial or other feedback

    Side effects
    ------------
    - Prints a human-review header and calls print_bill_table(state.get("parsed_bill", {}))
      and print_validation_result(state.get("parsed_bill", {})).
    - Ensures the directory "c:\\temp" exists and attempts to write the entire state
      as JSON to "c:\\temp\\state.json" (UTF-8, indented). If writing fails, an
      error message is printed to stdout.
    - Blocks for interactive input via input(...). Not suitable for non-interactive
      environments (e.g., background services, CI) without a connected TTY.

    Notes
    -----
    - This function does not raise on file write failure; it prints an error and continues.
    - The function is intended for manual human-in-the-loop review steps and will
      pause execution until the user provides input.
    """
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