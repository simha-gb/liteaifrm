from tools.local_code_interpreter import run_code

def run(input_data, config):
    code = input_data.get("code", "")
    # Здесь твой код для запуска (например, exec или subprocess)
    # Пример “эмуляции” запуска:
    try:
        # В реальности лучше запускать через subprocess/PythonExecutor ради безопасности!
        local_vars = {}
        exec(code, {}, local_vars)
        stdout = local_vars.get('stdout', '')
    except Exception as e:
        stdout = ""
        stderr = str(e)
    else:
        stderr = ""
    result = dict(input_data)
    result["code_result"] = {"stdout": stdout, "stderr": stderr}
    # Для Gradio! Явно возвращаем final_answer
    result["final_answer"] = stdout or code or "No output"
    return result
