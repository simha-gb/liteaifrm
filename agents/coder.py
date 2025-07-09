from tools.local_code_interpreter import run_code
def run(input_data, config):
    code = input_data.get("code", "")
    code_result = run_code(code)
    result = dict(input_data)
    result["code_result"] = code_result
    result["final_answer"] = code_result["stdout"] or code or "No output"
    return result

