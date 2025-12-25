import json
import os
from langchain_google_genai import ChatGoogleGenerativeAI


# Initialize LLM once
llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0,
)


def clean_json_output(output: str) -> str:
    """
    Remove ```json ... ``` fences safely.
    """
    output = output.strip()

    if output.startswith("```json"):
        output = output[len("```json"):]

    if output.startswith("```"):
        output = output[len("```"):]

    if output.endswith("```"):
        output = output[:-3]

    return output.strip()


def extract_bill_with_gemini(raw_text: str, prompt: str, users: str) -> dict:
    """
    Calls Gemini with a structured prompt and extracts JSON output safely.
    """

    full_prompt = (
        f"{prompt}\n\n"
        "Use the user data below and add the name information:\n"
        "```json\n"
        f"{users}\n"
        "```\n"
        "-------------------------\n"
        "BILL TEXT:\n"
        "-------------------------\n"
        f"{raw_text}\n\n"
        "Return ONLY valid JSON.\n"
    )

    print("Invoking Gemini for bill extraction...")

    response = llm.invoke(full_prompt)

    # Gemini sometimes returns list of dicts, sometimes a single string
    if hasattr(response, "content"):
        if isinstance(response.content, list):
            output = "".join(
                part.get("text", "")
                for part in response.content
                if isinstance(part, dict)
            )
        else:
            output = str(response.content)
    else:
        output = str(response)

    output = output.strip()
    cleaned = clean_json_output(output)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {
            "error": "Gemini returned non‑JSON output",
            "raw_output": output,
            "cleaned_output": cleaned,
        }