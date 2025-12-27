from typing import List, TypedDict, Optional, Dict, Any

class AgentState(TypedDict):
    pdf_file_name: Optional[str]
    raw_bill_text: Optional[str]
    parsed_bill: Optional[Dict[str, Any]]
    human_feedback: Optional[str]
    upload_status: Optional[str]
    retry_count: int
    chat_history: List[dict]