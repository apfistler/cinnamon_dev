#lib/yaml_parser.py

import yaml
import re
import os

class YamlParser:
    @staticmethod
    def parse_yaml(file_path):
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)

    @staticmethod
    def handle_placeholders(value, data):
        if isinstance(value, dict):
            return {k: YamlParser.handle_placeholders(v, data) for k, v in value.items()}
        elif isinstance(value, list):
            return [YamlParser.handle_placeholders_in_array(item, data) for item in value]
        elif isinstance(value, str):
            return YamlParser.handle_placeholders_in_string(value, data)
        else:
            return value

    def handle_placeholders_in_array(array, data):
        if isinstance(array, (dict, list)):
            return [
                YamlParser.handle_placeholders(item, data) if isinstance(item, (dict, list)) else item
                for item in array
            ]
        else:
            return array

    @staticmethod
    def handle_placeholders_in_string(value, data):
        def replace_placeholder(match):
            placeholder = match.group(1) or match.group(3)

            # Try to get the value from environment variables
            env_value = os.environ.get(placeholder)
            if env_value is not None:
                return env_value

            # Try to get the value from YAML data
            try:
                return str(YamlParser.get_nested_value(placeholder, data))
            except Exception:
                return match.group(0)

        # Replace both #{} and ${} placeholders iteratively until no more replacements are possible
        while re.search(r'#\{(\w+(\.\w+)*)\}|\${(\w+(\.\w+)*)}', value):
            value = re.sub(r'#\{(\w+(\.\w+)*)\}|\${(\w+(\.\w+)*)}', replace_placeholder, value)

        return value

    @staticmethod
    def get_nested_value(nested_key, data, visited_keys=None):
        if visited_keys is None:
            visited_keys = set()

        keys = nested_key.split('.')
        current_data = data

        for key in keys:
            if key in visited_keys:
                raise ValueError(f"Circular reference detected for key '{key}' in '{nested_key}'")

            visited_keys.add(key)

            if isinstance(current_data, dict) and key in current_data:
                current_data = current_data[key]
            elif isinstance(current_data, list) and key.isdigit() and 0 <= int(key) < len(current_data):
                current_data = current_data[int(key)]
            else:
                return f"Value for '{nested_key}' not found"

        return current_data

    @staticmethod
    def parse_properties(config, data):
        for key, value in config.items():
            config[key] = YamlParser.handle_placeholders(value, data)

    @staticmethod
    def validate_required_fields(config, required_fields):
        for field in required_fields:
            if field not in config:
                return f"Required field '{field}' not found in config"

    @staticmethod
    def display_property(value, indent=0):
        if isinstance(value, dict):
            for key, subvalue in value.items():
                print(" " * indent + f"{key}:")
                YamlParser.display_property(subvalue, indent + 2)
        elif isinstance(value, list):
            for item in value:
                YamlParser.display_property(item, indent)
        else:
            print(" " * indent + f"{value}")
