from state import AgentState
from typing import Dict, Any

def increment_retry(state: Dict[str, Any]) -> Dict[str, Any]:
    state["retry_count"] = state.get("retry_count", 0) + 1
    return state