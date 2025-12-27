from typing import Dict, Any
from services.llm_service import extract_bill_with_gemini
from services.user_service import get_user_data
import state
from utils.prompt_loader import load_prompt
import json
import os

  
def get_bill_info(state: Dict[str, Any]) -> Dict[str, Any]:

    retry_count = state["retry_count"]
    print(f"Extracting bill info using Gemini (Attempt #{retry_count + 1})...")

    raw_text = state["raw_bill_text"]
    base_prompt = load_prompt()
    users = get_user_data()

    # Build enhanced prompt
    chat_history = state.get("chat_history", [])
    validation_msg = state.get("validation", {}).get("validation_message", "")

    retry_context = ""

    if retry_count > 0:
        retry_context = (
            "\n\nPrevious attempt failed validation.\n"
            f"Validation message: {validation_msg}\n\n"
            "Here is the previous conversation:\n"
        )
        for msg in chat_history:
            retry_context += f"{msg['role']}: {msg['content']}\n"

    final_prompt = base_prompt + retry_context

    parsed_bill = extract_bill_with_gemini(
        raw_text=raw_text,
        prompt=final_prompt,
        users=users
    )

    # Save LLM output into chat history
    new_history = chat_history + [{
        "role": "assistant",
        "content": str(parsed_bill)
    }]

    return {**state, "parsed_bill": parsed_bill, "chat_history": new_history}