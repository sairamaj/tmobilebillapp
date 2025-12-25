import json
import os
from db import upload


def save_temp_bill(parsed_bill, path: str = r"C:\temp\test.json") -> None:
    """
    Save the parsed bill JSON to a temporary file for human review.
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(parsed_bill, f, indent=2, ensure_ascii=False)

        print(f"Saved parsed bill to {path}")

    except Exception as e:
        print(f"Failed to save parsed bill: {e}")


def upload_to_db(parsed_bill) -> str:
    """
    Upload the parsed bill to DynamoDB (or any DB via db.upload).
    Returns a status string.
    """
    try:
        upload(parsed_bill)
        return "SUCCESS"
    except Exception as e:
        print(f"Upload failed: {e}")
        return "FAILED"