import os
import re
import hashlib

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
    def calculate_checksum(file_path, algorithm="sha256"):
        """Calculate the checksum of a file."""
        hash_algorithm = hashlib.new(algorithm)

        with open(file_path, "rb") as file:
            # Read the file in chunks to avoid loading the entire file into memory
            chunk_size = 8192
            for chunk in iter(lambda: file.read(chunk_size), b""):
                hash_algorithm.update(chunk)

        return hash_algorithm.hexdigest()

    def mkdir(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def merge_dicts(*dicts):
        """
        Merge dictionaries with existing attributes recursively.
        If an attribute is an array or a dictionary, merge them.
        If it's any other type, overwrite the existing value.

        Args:
            *dicts (dict): Variable number of dictionaries to merge.

        Returns:
            dict: The merged dictionary.
        """
        merged_dict = {}

        for d in dicts:
            for key, value in d.items():
                if key in merged_dict and isinstance(merged_dict[key], dict) and isinstance(value, dict):
                    # If the attribute is a dictionary, merge them recursively
                    merged_dict[key] = Common.merge_dicts(merged_dict[key], value)
                elif key in merged_dict and isinstance(merged_dict[key], list) and isinstance(value, list):
                    # If the attribute is a list, merge them
                    merged_dict[key].extend(value)
                else:
                    # For other types or new keys, overwrite the existing value
                    merged_dict[key] = value

        return merged_dict

