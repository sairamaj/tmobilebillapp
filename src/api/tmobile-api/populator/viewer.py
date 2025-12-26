"""
viewer.py
Rich-based bill viewer for T-Mobile billing data.
"""

from typing import Dict, Any

from rich.console import Console
from rich.table import Table
from rich import box
from rich.panel import Panel
from rich.text import Text

console = Console()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def fmt_currency(value: Any) -> str:
    """Format a numeric value as currency with optional negative highlighting."""
    try:
        value = float(value)
    except (TypeError, ValueError):
        value = 0.0

    return f"[red]{value:.2f}[/red]" if value < 0 else f"{value:.2f}"


def add_summary_row(table: Table, label: str, value: Any, highlight: bool = False) -> None:
    """Add a row to the summary table with optional highlighting."""
    formatted = fmt_currency(value)
    if highlight:
        formatted = f"[bold magenta]{formatted}[/bold magenta]"
    table.add_row(label, formatted)


# ---------------------------------------------------------------------------
# Main Rendering Function
# ---------------------------------------------------------------------------

def print_bill_table(parsed_bill: Dict[str, Any]) -> None:
    """
    Render a T-Mobile bill using Rich tables.

    Expected parsed_bill structure:
    {
        "bill_summary": {...},
        "line_items": { "1234567890": {...}, ... }
    }
    """
    if not isinstance(parsed_bill, dict):
        console.print("[red]Error: parsed_bill must be a dictionary[/red]")
        return

    lines = parsed_bill.get("line_items", {})
    summary = parsed_bill.get("bill_summary", {})

    # -----------------------------------------------------------------------
    # Line-by-line table
    # -----------------------------------------------------------------------
    table = Table(
        title="📱 T‑Mobile Bill — Line‑by‑Line Breakdown",
        box=box.ROUNDED,
        show_lines=False,
        header_style="bold magenta",
    )

    table.add_column("Line", style="white", no_wrap=True)
    table.add_column("Name", style="white")
    table.add_column("Plan", justify="right", style="cyan")
    table.add_column("Equipment", justify="right", style="green")
    table.add_column("Services", justify="right", style="yellow")
    table.add_column("Total", justify="right", style="magenta")

    if isinstance(lines, dict):
        for line, data in lines.items():
            name = data.get("name", "")
            plan = data.get("plan", 0)
            equip = data.get("equipment", 0)
            svc = data.get("services", 0)
            total = data.get("total", 0)

            table.add_row(
                str(line),
                name,
                fmt_currency(plan),
                fmt_currency(equip),
                fmt_currency(svc),
                fmt_currency(total),
            )
    else:
        console.print("[yellow]Warning: line_items is not a dictionary[/yellow]")

    console.print(table)

    # -----------------------------------------------------------------------
    # Summary table
    # -----------------------------------------------------------------------
    summary_table = Table(
        title="📊 Summary",
        box=box.SIMPLE_HEAVY,
        header_style="bold blue",
    )

    summary_table.add_column("Category", style="white")
    summary_table.add_column("Amount", justify="right", style="bold")

    add_summary_row(summary_table, "Per Line Plan Amount", summary.get("per_line_plan_amount"))
    add_summary_row(summary_table, "Equipment Total", summary.get("equipment_total"))
    add_summary_row(summary_table, "Services Total", summary.get("services_total"))
    add_summary_row(summary_table, "Grand Total", summary.get("total_amount"), highlight=True)

    console.print(summary_table)

def print_validation_result(state: dict):
    """
    Pretty‑prints validation_flag and validation_message using Rich.
    """

    flag = state.get("validation_flag", False)
    message = state.get("validation_message", "")
    
    if flag:
        color = "green"
        title = "VALIDATION PASSED"
    else:
        color = "red"
        title = "VALIDATION FAILED"

    console.print(
        Panel(
            Text(message, style=color),
            title=title,
            border_style=color
        )
    )