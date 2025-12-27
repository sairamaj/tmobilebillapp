from langgraph.graph import StateGraph, END

def validate_bill(state):
    print("Validating bill information...")
    validated = validate_bill_info(state["parsed_bill"])
    print(f"Validation result: {validated.get('validation_flag')}, Message: {validated.get('validation_message')}")
    return {**state, "validation": validated}

def validate_bill_info(bill_info: dict) -> dict:
    """
    Validates the bill information extracted from the T-Mobile PDF.

    Rules:
    1. Every line must have the same plan amount.
    2. total_lines * plan + equipment_total + services_total ≈ total_amount (within $1).
    """

    line_items = bill_info.get("line_items", {})
    summary = bill_info.get("bill_summary", {})

    # Extract plan amounts
    plan_amounts = {item["plan"] for item in line_items.values()}
    same_plan = len(plan_amounts) == 1

    # If plan amounts differ, validation fails immediately
    if not same_plan:
        bill_info["validation_flag"] = False
        bill_info["validation_message"] = "Plan amounts differ across lines."
        return bill_info

    # Use the common plan amount
    plan_amount = plan_amounts.pop()
    total_lines = len(line_items)

    # Compute expected total
    expected_total = round(
        (plan_amount * total_lines)
        + summary.get("equipment_total", 0)
        + summary.get("services_total", 0),
        2
    )

    actual_total = round(summary.get("total_amount", 0), 2)

    # Allow $1 variation
    within_tolerance = abs(expected_total - actual_total) <= 1.0

    bill_info["validation_flag"] = same_plan and within_tolerance
    bill_info["validation_message"] = (
        f"Expected total: {expected_total}, Actual total: {actual_total}, "
        f"Within tolerance: {within_tolerance}"
    )

    return bill_info