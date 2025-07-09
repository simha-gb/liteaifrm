"""Simple reflection agent.

This agent inspects the result of the previous step and can request a retry
when it detects an error. It expects the input to be a dictionary created by
other agents.
"""

def run(input_data, config):
    # If previous step produced an error in ``code_result``, ask for a retry.
    code_res = None
    if isinstance(input_data, dict):
        code_res = input_data.get("code_result")
    if code_res and code_res.get("stderr"):
        # Request to redo the last agent without modifications
        return {"redo": True}
    return {}
