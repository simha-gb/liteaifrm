from tools.local_code_interpreter import run_code
from utils.rag import search
def run(input_data, config):
    code = input_data.get("code", "")

    # Retrieve context if enabled
    retriever_cfg = config.get("retriever", {})
    context_text = ""
    if retriever_cfg.get("enabled"):
        chunks = search(code, retriever_cfg, config)
        context_text = "\n".join([c["content"] for c in chunks])

    code_result = run_code(code)
    result = dict(input_data)
    result["code_result"] = code_result
    result["final_answer"] = code_result["stdout"] or code or "No output"
    if context_text:
        result["retrieved_context"] = context_text
    return result

