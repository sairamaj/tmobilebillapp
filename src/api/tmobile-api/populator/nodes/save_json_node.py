import os
import json
from typing import Dict, Any

def save_parsed_bill(state: Dict[str, Any]) -> Dict[str, Any]:
    """LangGraph node: save the `parsed_bill` JSON to cached/{month}.json.
    
    - Uses parsed_bill["bill_summary"]["month"] directly (e.g. "May2025")
    - Overwrites existing files
    - Adds saved_bill_path to state
    """
    parsed = state.get("parsed_bill")
    if not parsed:
        print("No parsed_bill in state; skipping save_parsed_bill")
        return state

    summary = parsed.get("bill_summary", {})
    month_value = summary.get("month")
    if not month_value:
        raise ValueError("parsed_bill['bill_summary']['month'] is missing")

    # Ensure directory exists
    cache_dir = "cached"
    os.makedirs(cache_dir, exist_ok=True)

    # File path uses month directly
    file_path = os.path.join(cache_dir, f"{month_value}.json")

    # Overwrite file
    with open(file_path, "w") as f:
        json.dump(parsed, f, indent=2)

    # Update state
    state["saved_bill_path"] = file_path
    state["bill_month"] = month_value

    return state