import sys
import io
import traceback

def execute_python_code(code):
    """
    Execute a block of Python code and return the stdout/stderr.
    """
    # Create buffers to capture stdout and stderr
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    
    # Redirect stdout and stderr
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = stdout_buffer
    sys.stderr = stderr_buffer
    
    # Execution namespace
    namespace = {}
    
    try:
        # We use exec() to run the code
        exec(code, namespace)
        success = True
    except Exception:
        # Capture the traceback if an error occurs
        traceback.print_exc()
        success = False
    finally:
        # Restore stdout and stderr
        sys.stdout = old_stdout
        sys.stderr = old_stderr
    
    output = stdout_buffer.getvalue()
    error = stderr_buffer.getvalue()
    
    result = {
        "success": success,
        "output": output,
        "error": error
    }
    
    # Format a summary for the AI
    if success:
        return f"Code executed successfully.\nOutput:\n{output if output else '[No output]'}"
    else:
        return f"Code execution failed.\nError:\n{error}"
