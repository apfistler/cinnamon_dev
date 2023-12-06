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
                if file.lower() == filename.lower():
                    full_path = os.path.join(root, file)
                    matches.append(full_path)
        return matches

    @staticmethod
    def file_exists(file_path):
        return os.path.exists(file_path)

    @staticmethod
    def merge_dicts(target, *new_dicts):
        """
        Merge dictionaries with existing attributes recursively.
        If an attribute is an array or a dictionary, merge them.
        If it's any other type, overwrite the existing value.

        Args:
            target (object): The target object to merge dictionaries into.
            *new_dicts (dict): Variable number of dictionaries to merge.

        Returns:
            None
        """
        for new_dict in new_dicts:
            for key, value in new_dict.items():
                if hasattr(target, key):
                    current_value = getattr(target, key)

                    # If the attribute is a dictionary, merge them recursively
                    if isinstance(current_value, dict) and isinstance(value, dict):
                        Common._merge_dicts_recursive(current_value, value)
                    # If the attribute is a list, merge them
                    elif isinstance(current_value, list) and isinstance(value, list):
                        current_value.extend(value)
                    # For other types, overwrite the existing value
                    else:
                        setattr(target, key, value)
                else:
                    setattr(target, key, value)

    @staticmethod
    def _merge_dicts_recursive(dict1, dict2):
        """
        Recursively merge two dictionaries.

        Args:
            dict1 (dict): The first dictionary.
            dict2 (dict): The second dictionary.

        Returns:
            None
        """
        for key, value in dict2.items():
            if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
                Common._merge_dicts_recursive(dict1[key], value)
            else:
                dict1[key] = value

