import argparse
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