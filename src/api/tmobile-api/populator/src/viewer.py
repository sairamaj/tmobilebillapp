# viewer.py
# Beautiful Rich-based bill viewer

from rich.console import Console
from rich.table import Table
from rich import box

console = Console()


def print_bill_table(parsed_bill: dict):
    lines = parsed_bill.get("line_items", {})
    summary = parsed_bill.get("bill_summary", {})

    # Create table
    table = Table(
        title="📱 T‑Mobile Bill — Line‑by‑Line Breakdown",
        box=box.ROUNDED,
        show_lines=False,
        header_style="bold magenta"
    )

    table.add_column("Line", style="white", no_wrap=True)
    table.add_column("Name", style="white")
    table.add_column("Plan", justify="right", style="cyan")
    table.add_column("Equipment", justify="right", style="green")
    table.add_column("Services", justify="right", style="yellow")
    table.add_column("Total", justify="right", style="magenta")

    # Add rows
    for line, data in lines.items():
        name = data.get("name", "")
        plan = data.get("plan", 0)
        equip = data.get("equipment", 0)
        svc = data.get("services", 0)
        total = data.get("total", 0)

        # Highlight negative values
        def fmt(val):
            return f"[red]{val:.2f}[/red]" if val < 0 else f"{val:.2f}"

        table.add_row(
            line,
            name,
            fmt(plan),
            fmt(equip),
            fmt(svc),
            fmt(total),
        )

    console.print(table)

    # Summary table
    summary_table = Table(
        title="📊 Summary",
        box=box.SIMPLE_HEAVY,
        header_style="bold blue"
    )

    summary_table.add_column("Category", style="white")
    summary_table.add_column("Amount", justify="right", style="bold")

    summary_table.add_row("Plan Total", f"{summary.get('total_plan_amount_generated', 0):.2f}")
    summary_table.add_row("Equipment Total", f"{summary.get('equipment_total', 0):.2f}")
    summary_table.add_row("Services Total", f"{summary.get('services_total', 0):.2f}")
    summary_table.add_row("Grand Total", f"[bold magenta]{summary.get('total_amount', 0):.2f}[/bold magenta]")

    console.print(summary_table)