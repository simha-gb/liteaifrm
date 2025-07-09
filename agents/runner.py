# MIT License
#
# Copyright (c) 2025 simha-gb
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
    result["final_answer"] = stdout or code or "No output"    return result