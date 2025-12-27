from typing import Dict, Any
from services.llm_service import extract_bill_with_gemini
from services.user_service import get_user_data
import state
from utils.prompt_loader import load_prompt
import json
import os

  
def get_bill_info(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract bill information from provided state using the Gemini-based extractor.
    Parameters
    ----------
    state : Dict[str, Any]
        Dictionary containing the input context. Required keys:
        - "raw_bill_text" (str): the raw bill text to be parsed.
        - "retry_count" (int): current retry/attempt count (used for logging).
        Any additional keys present in `state` will be preserved and returned.
    Returns
    -------
    Dict[str, Any]
        A new dict merged from the input `state` with an added key:
        - "parsed_bill": the parsed result returned by extract_bill_with_gemini(raw_text, prompt, users).
    Side effects
    ------------
    - Loads a prompt via load_prompt() and user-specific data via get_user_data().
    - Calls extract_bill_with_gemini(...) which may perform I/O or external API calls.
    - Prints a status message to stdout indicating the extraction attempt number.
    Exceptions
    ----------
    - KeyError: if required keys ("raw_bill_text" or "retry_count") are missing from `state`.
    - Propagates exceptions from load_prompt(), get_user_data(), or extract_bill_with_gemini()
      (for example, configuration, network, or API errors).
    Notes
    -----
    - The exact structure of "parsed_bill" is determined by extract_bill_with_gemini and
      is not specified here.
    """

    retry_count = state["retry_count"]
    print("Extracting bill info using Gemini (Attempt #{})...".format(retry_count + 1))

    raw_text = state["raw_bill_text"]
    prompt = load_prompt()
    users = get_user_data()

    parsed_bill = extract_bill_with_gemini(raw_text, prompt, users)
    return {**state, "parsed_bill": parsed_bill}