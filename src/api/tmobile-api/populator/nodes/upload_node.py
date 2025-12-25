from typing import Dict, Any
from services.storage_service import upload_to_db

def upload_to_dynamodb(state: Dict[str, Any]) -> Dict[str, Any]:
    print("\nUploading bill to DynamoDB...")
    status = upload_to_db(state["parsed_bill"])
    return {**state, "upload_status": status}