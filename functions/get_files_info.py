import os

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) 
        if not valid_target_dir == working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        record=[]
        for item in os.listdir(target_dir):
            record.append(f"- {item}: file_size={os.path.getsize(os.path.join(target_dir,item))} bytes, is_dir={os.path.isdir(os.path.join(target_dir, item))}")
        return "\n".join(record)
    except Exception as e:
        return f"Error: {e}"
