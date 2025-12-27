from typing import Dict, Any
from services.storage_service import upload_to_db

def upload_to_dynamodb(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Upload the parsed bill data to DynamoDB and extend the provided state with the upload result.

    Parameters
    ----------
    state : Dict[str, Any]
        A mapping representing the current workflow state. Must contain the key "parsed_bill"
        whose value is the bill data to upload.

    Returns
    -------
    Dict[str, Any]
        A new state dictionary that preserves all original keys and adds an "upload_status" key
        with the value returned by upload_to_db(state["parsed_bill"]).

    Side effects
    ------------
    - Prints a status message to stdout.
    - Calls upload_to_db(parsed_bill) to perform the actual DynamoDB upload; any exceptions
      raised by upload_to_db will propagate to the caller.

    Notes
    -----
    - This function does not validate the structure of "parsed_bill"; validation (if needed)
      should be performed before calling this function.
    """
    print("\nUploading bill to DynamoDB...")
    status = upload_to_db(state["parsed_bill"])
    return {**state, "upload_status": status}