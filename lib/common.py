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

    @staticmethod
    def find_files_by_partial_name(search_path, partial_name):
        matches = []
        partial_name_parts = partial_name.split('/')
        for root, dirs, files in os.walk(search_path):

            if not partial_name in partial_name_parts:
                continue

            for filename in files:
                if partial_name.lower() in filename.lower():
                    full_path = os.path.join(root, filename)
                    matches.append(full_path)

        return matches

    @staticmethod
    def find_files_by_name(directory, filename):
        matches = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                print(f"{file}")
                if file.lower() == filename.lower():
                    full_path = os.path.join(root, file)
                    matches.append(full_path)
        return matches

    @staticmethod
    def file_exists(file_path):
        return os.path.exists(file_path)

