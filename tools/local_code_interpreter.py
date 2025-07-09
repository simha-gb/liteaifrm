import sys
import io

def run_code(code):
    # Очень упрощенный sandbox — запуск кода в string (дальше можно добавить ограничение импорта, времени, и т.д.)
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = mystdout = io.StringIO()
    sys.stderr = mystderr = io.StringIO()
    try:
        exec(code, {})  # В реале надо sandbox
        result = mystdout.getvalue()
        error = mystderr.getvalue()
    except Exception as e:
        result = ""
        error = str(e)
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
    return {"stdout": result, "stderr": error}
