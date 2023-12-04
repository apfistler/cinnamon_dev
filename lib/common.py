import os
import re

class Common:
    @staticmethod
    def clean_path(path):
        return re.sub(r'^[/.\W_]+', '', path)

    @staticmethod
    def get_files_recursively(directory):
        file_dict = {}
        for root, dirs, files in os.walk(directory):
            for filename in files:
                relative_path = os.path.relpath(os.path.join(root, filename), directory)
                full_path = os.path.join(root, filename)
                file_dict[full_path] = {
                    'filename': filename,
                    'relative_path': relative_path,
                    'full_path': full_path
                }
        return file_dict

