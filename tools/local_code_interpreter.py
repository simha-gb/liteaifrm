"""Helpers for executing code snippets.

WARNING: running untrusted code is dangerous. Use a proper sandbox in production.
"""

import sys
import io


def run_code(code):
    """Execute code and capture stdout/stderr. No sandboxing!"""
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = mystdout = io.StringIO()
    sys.stderr = mystderr = io.StringIO()
    try:
        exec(code, {})
        result = mystdout.getvalue()
        error = mystderr.getvalue()
    except Exception as e:
        result = ""
        error = str(e)
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
    return {"stdout": result, "stderr": error}
