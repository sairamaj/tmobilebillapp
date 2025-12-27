from typing import Dict, Any
from services.llm_service import extract_bill_with_gemini
from services.user_service import get_user_data
import state
from utils.prompt_loader import load_prompt
import json
import os

  
def get_bill_info(state: Dict[str, Any]) -> Dict[str, Any]:

    retry_count = state["retry_count"]
    print("Extracting bill info using Gemini (Attempt #{})...".format(retry_count + 1))

    raw_text = state["raw_bill_text"]
    prompt = load_prompt()
    users = get_user_data()

    #parsed_bill = extract_bill_with_gemini(raw_text, prompt, users)
    file_path = r"C:\temp\test.json"
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Parsed bill file not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        parsed_bill = json.load(f)
    return {**state, "parsed_bill": parsed_bill}