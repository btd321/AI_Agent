import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs,file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) 
        if not valid_target_dir == working_dir_abs:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'
    
        with open(target_dir, "r") as f:
            file_content_string = f.read(MAX_CHARS)
    
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    
        return file_content_string
    
    except Exception as e:
        return f"Error:{e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Displays content of file provided working directory and file path",
    parameters=types.Schema(
        required = ["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to the content to be displayed",
            ),
        },
    ),
)