# view_workflow.py

import os
import subprocess
import webbrowser
from workflow import build_workflow   # your import

def save_and_view_workflow():
    app = build_workflow()

    out_dir = "workflow_diagrams"
    os.makedirs(out_dir, exist_ok=True)

    # --- Save Mermaid diagram ---
    mermaid_path = os.path.join(out_dir, "workflow_graph.mmd")
    mermaid_text = app.get_graph().draw_mermaid()

    with open(mermaid_path, "w") as f:
        f.write(mermaid_text)

    print(f"Saved Mermaid diagram → {mermaid_path}")

    # --- Convert Mermaid → PNG using Mermaid CLI ---
    #png_path = os.path.join(out_dir, "workflow_graph.png")

    # try:
    #     subprocess.run(
    #         ["mmdc", "-i", mermaid_path, "-o", png_path],
    #         check=True
    #     )
    #     print(f"Rendered PNG diagram → {png_path}")
    # except Exception as e:
    #     print("Error running Mermaid CLI (mmdc). Is it installed globally?")
    #     print(e)
    #     return

    # --- Open PNG ---
    #webbrowser.open(f"file://{os.path.abspath(png_path)}")


if __name__ == "__main__":
    save_and_view_workflow()