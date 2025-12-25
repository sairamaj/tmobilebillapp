from typing import Dict, Any
from services.llm_service import extract_bill_with_gemini
from services.user_service import get_user_data
from utils.prompt_loader import load_prompt

def get_bill_info(state: Dict[str, Any]) -> Dict[str, Any]:
    print("Extracting bill info using Gemini...")

    raw_text = state["raw_bill_text"]
    prompt = load_prompt()
    users = get_user_data()

    parsed_bill = extract_bill_with_gemini(raw_text, prompt, users)

    return {**state, "parsed_bill": parsed_bill}