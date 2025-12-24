from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional, Dict, Any
import pdfplumber
from langchain_google_genai import ChatGoogleGenerativeAI
import json
import os
import argparse, os, sys
from db import upload
from viewer import print_bill_table

llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0,
)
def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def load_prompt(path: str = "prompt.txt") -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def extract_bill_with_gemini(raw_text: str, prompt: str) -> dict:
    full_prompt = f"""
{prompt}

-------------------------
BILL TEXT:
-------------------------
{raw_text}

Return ONLY valid JSON.
"""
    print("Invoking Gemini for bill extraction...")
    response = llm.invoke(full_prompt)

    # Combine all text parts
    output = "".join(
        part["text"] for part in response.content 
        if isinstance(part, dict) and "text" in part
    ).strip()

    # Clean JSON if wrapped in ```json fences
    cleaned = output.strip("```json").strip("```").strip()

    try:
        data = json.loads(cleaned)
        return data
    except json.JSONDecodeError:
        return {
            "error": "Gemini returned non‑JSON output",
            "raw_output": output
        }
# ---------------------------------------------------------
# 1. Define the State
# ---------------------------------------------------------
class AgentState(TypedDict):
    raw_bill_text: Optional[str]
    parsed_bill: Optional[Dict[str, Any]]
    human_feedback: Optional[str]
    upload_status: Optional[str]

def get_bill_info(state: AgentState) -> AgentState:
    print("Extracting bill info using Gemini...")

    raw_text = state["raw_bill_text"]
    prompt = load_prompt("prompt.txt")

    #parsed_bill = extract_bill_with_gemini(raw_text, prompt)
    parsed_bill = None
    tmp_path = r"C:\temp\test.json"
    if os.path.exists(tmp_path):
        try:
            with open(tmp_path, "r", encoding="utf-8") as f:
                parsed_bill = json.load(f)
            print(f"Loaded parsed bill from {tmp_path}")
        except Exception as e:
            print(f"Failed to load {tmp_path}: {e}")

    if parsed_bill is None:
        parsed_bill = extract_bill_with_gemini(raw_text, prompt)

    return {
        **state,
        "parsed_bill": parsed_bill
    }


# ---------------------------------------------------------
# 3. Node: Human Review
# ---------------------------------------------------------
def human_review(state: AgentState) -> AgentState:
    """
    Human-in-the-loop approval step.
    """
    print("\n--- HUMAN REVIEW REQUIRED ---")
    print("Bill details:", state["parsed_bill"])
    print_bill_table(state["parsed_bill"])

    try:
        os.makedirs(r"C:\temp", exist_ok=True)
        with open(r"C:\temp\test.json", "w", encoding="utf-8") as f:
            json.dump(state["parsed_bill"], f, indent=2, ensure_ascii=False)
        print(r"Saved parsed bill to C:\temp\test.json")
    except Exception as e:
        print(f"Failed to save parsed bill: {e}")

    feedback = input("Enter 'approve' to continue or anything else to deny: ").strip().lower()

    return {
        **state,
        "human_feedback": feedback
    }


# ---------------------------------------------------------
# 4. Conditional routing based on human approval
# ---------------------------------------------------------
def review_condition(state: AgentState):
    """
    Route based on human feedback.
    """
    if state["human_feedback"] == "approve":
        return "approved"
    return "denied"


# ---------------------------------------------------------
# 5. Node: Upload to DynamoDB
# ---------------------------------------------------------
def upload_to_dynamodb(state: AgentState) -> AgentState:
    """
    Placeholder for DynamoDB upload.
    Replace with boto3 logic.
    """
    print("\nUploading bill to DynamoDB...")
    db.upload(state["parsed_bill"])
    # TODO: boto3 DynamoDB put_item()
    upload_status = "SUCCESS"

    return {
        **state,
        "upload_status": upload_status
    }


# ---------------------------------------------------------
# 6. Build the Graph
# ---------------------------------------------------------
workflow = StateGraph(AgentState)

workflow.add_node("get_bill_info", get_bill_info)
workflow.add_node("human_review", human_review)
workflow.add_node("upload_to_dynamodb", upload_to_dynamodb)

workflow.set_entry_point("get_bill_info")

# Normal edge
workflow.add_edge("get_bill_info", "human_review")

# Conditional edge from human review
workflow.add_conditional_edges(
    "human_review",
    review_condition,
    {
        "approved": "upload_to_dynamodb",
        "denied": END
    }
)

# End after DynamoDB upload
workflow.add_edge("upload_to_dynamodb", END)

app = workflow.compile()


# ---------------------------------------------------------
# 7. Run the Workflow
# ---------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract bill text from a PDF and run the upload workflow.")
    parser.add_argument("pdf_path", help="Path to the PDF file")
    args = parser.parse_args()

    pdf_path = args.pdf_path

    if not os.path.isfile(pdf_path):
        print(f"Error: file not found: {pdf_path}")
        sys.exit(1)
    bill_text = extract_text_from_pdf(pdf_path)

    initial_state = {
        "raw_bill_text": bill_text,
        "parsed_bill": None,
        "human_feedback": None,
        "upload_status": None
    }

    result = app.invoke(initial_state)
    #print("\n--- FINAL RESULT ---")
    #print(result)