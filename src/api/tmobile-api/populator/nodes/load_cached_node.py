import os
import json
from typing import Dict, Any

def load_cached_bill(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Load cached bill JSON based on the PDF filename in state["pdf_file_name"].

    Expected filename format:
        SummaryBillMay2025.pdf

    This extracts "May2025" and loads:
        cached/May2025.json
    """
    pdf_name = state.get("pdf_file_name")
    if not pdf_name:
        raise ValueError("State missing 'pdf_file_name'")

    print(f"Looking for cached bill for PDF: {pdf_name}")

    # --- Strip extension (.pdf or anything else) ---
    pdf_base, _ = os.path.splitext(pdf_name)   # "SummaryBillMay2025"

    # --- Extract month portion ---
    prefix = "SummaryBill"
    if not pdf_base.startswith(prefix):
        raise ValueError(f"Unexpected pdf_file_name format: {pdf_name}")

    month_value = pdf_base[len(prefix):]       # "May2025"

    # --- Build path to cached JSON ---
    cache_path = os.path.join("cached", f"{month_value}.json")

    if not os.path.exists(cache_path):
        print(f"Cache file does not exist: {cache_path}")
        return state  # No cached bill → parsed_bill stays None

    # --- Load cached JSON ---
    with open(cache_path, "r") as f:
        cached_bill = json.load(f)
    print(f"Loaded cached bill from {cache_path}")
    # Update state
    state["parsed_bill"] = cached_bill
    state["cached_bill_path"] = cache_path
    state["bill_month"] = month_value

    print(f"Loaded cached bill: {cache_path}")

    return state