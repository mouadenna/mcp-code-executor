from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
import tempfile
import os
import subprocess
import time

mcp = FastMCP("CodeExecutor", host="127.0.0.1", port=8000)

@mcp.tool()
async def execute_code(language: str, code: str) -> Dict[str, Any]:
    """
    Executes code in the specified programming language.
    
    Parameters:
    - language: The programming language (java, python, javascript, typescript, cpp)
    - code: The source code to execute
    
    Returns:
    - output: The standard output of the execution
    - error: Any error messages
    - exitCode: The exit code of the execution
    - timeout: Whether the execution timed out
    """
    print("Executing code...")
    print(code)
    executor = CodeExecutor()
    return executor.execute(language, code)

class CodeExecutor:
    MAX_EXECUTION_TIME = 10  # seconds
    
    def execute(self, language: str, code: str) -> Dict[str, Any]:
        try:
            if language.lower() == "cpp":
                return self.execute_cpp(code)
            elif language.lower() == "python":
                return self.execute_python(code)
            elif language.lower() == "javascript":
                return self.execute_javascript(code)
            elif language.lower() == "typescript":
                return self.execute_typescript(code)
            elif language.lower() == "java":
                return self.execute_java(code)
            else:
                return {
                    "output": "",
                    "error": f"Unsupported language: {language}",
                    "exitCode": -1,
                    "timeout": False
                }
        except Exception as e:
            return {
                "output": "",
                "error": f"Execution error: {str(e)}",
                "exitCode": -1,
                "timeout": False
            }
    
    def execute_command(self, command: str, cwd: Optional[str] = None) -> Dict[str, Any]:
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=cwd
            )
            
            start_time = time.time()
            timeout = False
            
            while process.poll() is None:
                if time.time() - start_time > self.MAX_EXECUTION_TIME:
                    process.kill()
                    timeout = True
                    break
                time.sleep(0.1)
            
            stdout, stderr = process.communicate()
            exit_code = process.returncode if not timeout else -1
            
            return {
                "output": stdout,
                "error": stderr,
                "exitCode": exit_code,
                "timeout": timeout
            }
        except Exception as e:
            return {
                "output": "",
                "error": f"Command execution error: {str(e)}",
                "exitCode": -1,
                "timeout": False
            }
    
    def execute_cpp(self, code: str) -> Dict[str, Any]:
        with tempfile.TemporaryDirectory() as temp_dir:
            cpp_file = os.path.join(temp_dir, "temp.cpp")
            executable = os.path.join(temp_dir, "temp_prog")
            if os.name == "nt":  # Windows
                executable += ".exe"
            
            # Write code to file
            with open(cpp_file, "w") as f:
                f.write(code)
            
            # Compile
            compile_cmd = f"g++ -o {executable} {cpp_file} -std=c++17"
            compile_result = self.execute_command(compile_cmd, temp_dir)
            
            if compile_result["exitCode"] != 0:
                return compile_result
            
            # Run
            run_cmd = executable if os.name != "nt" else f"{executable}"
            return self.execute_command(run_cmd, temp_dir)
    
    def execute_python(self, code: str) -> Dict[str, Any]:
        with tempfile.TemporaryDirectory() as temp_dir:
            py_file = os.path.join(temp_dir, "temp.py")
            
            # Write code to file
            with open(py_file, "w") as f:
                f.write(code)
            
            # Run
            cmd = f"python {py_file}"
            return self.execute_command(cmd, temp_dir)
    
    def execute_javascript(self, code: str) -> Dict[str, Any]:
        with tempfile.TemporaryDirectory() as temp_dir:
            js_file = os.path.join(temp_dir, "temp.js")
            
            # Write code to file
            with open(js_file, "w") as f:
                f.write(code)
            
            # Run
            cmd = f"node {js_file}"
            return self.execute_command(cmd, temp_dir)
    
    def execute_typescript(self, code: str) -> Dict[str, Any]:
        with tempfile.TemporaryDirectory() as temp_dir:
            ts_file = os.path.join(temp_dir, "temp.ts")
            
            # Write TypeScript code to file
            with open(ts_file, "w") as f:
                f.write(code)
            
            # Compile TypeScript to JavaScript
            compile_cmd = f"tsc {ts_file}"
            compile_result = self.execute_command(compile_cmd, temp_dir)
            
            if compile_result["exitCode"] != 0:
                return compile_result
            
            # Run the compiled JavaScript
            js_file = os.path.join(temp_dir, "temp.js")
            run_cmd = f"node {js_file}"
            return self.execute_command(run_cmd, temp_dir)
    
    def execute_java(self, code: str) -> Dict[str, Any]:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extract the class name
            class_name = self.extract_class_name(code)
            java_file = os.path.join(temp_dir, f"{class_name}.java")
            
            # Write code to file
            with open(java_file, "w") as f:
                f.write(code)
            
            # Compile
            compile_cmd = f"javac {java_file}"
            compile_result = self.execute_command(compile_cmd, temp_dir)
            
            if compile_result["exitCode"] != 0:
                return compile_result
            
            # Run
            run_cmd = f"java -cp {temp_dir} {class_name}"
            return self.execute_command(run_cmd, temp_dir)
    
    def extract_class_name(self, code: str) -> str:
        default_name = "Main"
        
        try:
            class_pos = code.find("public class")
            if class_pos == -1:
                return default_name
            
            name_start = code.find(' ', class_pos + 12) + 1
            name_end = code.find(' ', name_start)
            
            if name_end == -1:
                name_end = code.find('{', name_start)
            
            if name_start == -1 or name_end == -1:
                return default_name
            
            return code[name_start:name_end].strip()
        except Exception:
            return default_name

if __name__ == "__main__":
    mcp.run(transport="sse") 