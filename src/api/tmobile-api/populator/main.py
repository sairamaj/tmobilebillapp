import argparse
"""
Command-line entry point for extracting text from a T-Mobile bill PDF and running an upload workflow.
This module is intended to be executed as a script (i.e. python -m or python main.py). It:
- Parses a single required command-line argument: the path to a PDF file.
- Validates that the file exists and is a regular file; exits with status code 1 and prints an error if not.
- Uses services.pdf_service.extract_text_from_pdf to extract raw text from the provided PDF.
- Constructs an initial workflow state dictionary containing metadata and placeholders:
    {
        "pdf_file_name": <basename of the PDF>,
        "raw_bill_text": <extracted text>,
- Builds a workflow application via workflow.build_workflow() and invokes it with the initial state.
- Prints the PDF file base name to stdout prior to invoking the workflow.
- Expects the workflow application to provide an invoke(initial_state) method that accepts and processes the state dict.
Usage:
    python main.py /path/to/bill.pdf
Dependencies:
- services.pdf_service.extract_text_from_pdf(pdf_path) -> str
- workflow.build_workflow() -> object with .invoke(state: dict) -> any
Side effects:
- Prints the PDF base name or an error message to stdout/stderr.
- Calls sys.exit(1) when the provided path is not a file.
Notes:
- This module is not intended to be imported for reuse; it performs CLI behavior only when executed as __main__.
- Any exceptions raised by extract_text_from_pdf or the workflow invocation will propagate unless handled by those functions.
"""
import os
import sys

from services.pdf_service import extract_text_from_pdf
from workflow import build_workflow

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
        "pdf_file_name": os.path.basename(pdf_path),
        "raw_bill_text": bill_text,
        "parsed_bill": None,
        "human_feedback": None,
        "upload_status": None,
        "retry_count": 0,
    }

    print(initial_state["pdf_file_name"])
    app = build_workflow()
    result = app.invoke(initial_state)