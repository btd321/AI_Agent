import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) 
        if not valid_target_dir == working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if file_path[(len(file_path)-3)::] != ".py":
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_dir]
        if args != None:
            command.extend(args)
        obj1 = subprocess.run(command,capture_output=True,cwd=working_dir_abs, timeout=30,text=True)
        report_string = ""
        string_list = []
        if obj1.returncode != 0:
            string_list.append(f"Process exited with code {obj1.returncode}")
        if obj1.stdout == "" and obj1.stderr == "":
            string_list.append("No output produced")
        if obj1.stdout:
            string_list.append(f"STDOUT:\n{obj1.stdout}")
        if obj1.stderr:
            string_list.append(f"STDERR:\n{obj1.stderr}")
        report_string = "\n".join(string_list)
        return report_string
    except Exception as e:
        return f"Error: executing Python file: {e}"    
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs python file with optional arguments",
    parameters=types.Schema(
        required = ["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File_path to file being run",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional arguments provided",
            )
        },
    ),
)