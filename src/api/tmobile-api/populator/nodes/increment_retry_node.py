from state import AgentState
"""
Increment the retry counter stored in a state dictionary.
This function updates the provided state mapping by incrementing the integer
value associated with the "retry_count" key. If that key does not exist, it
will be created and initialized to 1.
Parameters
----------
state : Dict[str, Any]
    A dictionary-like object representing agent state; this object is mutated
    in-place.
Returns
-------
Dict[str, Any]
    The same state mapping passed in, after updating "retry_count".
Raises
------
TypeError
    If an existing value for "retry_count" is not a number and cannot be
    incremented with +1.
Notes
-----
- The operation is performed in-place; callers expecting an immutable update
  should pass a copy of the state.
"""
from typing import Dict, Any

def increment_retry(state: Dict[str, Any]) -> Dict[str, Any]:
    state["retry_count"] = state.get("retry_count", 0) + 1
    return {**state, "retry_count": state["retry_count"]}