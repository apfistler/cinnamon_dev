#lib/yaml_parser.py

import yaml
import re

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

    @staticmethod
    def handle_placeholders_in_array(array, data):
        return [YamlParser.handle_placeholders_in_string(item, data) if isinstance(item, str) else YamlParser.handle_placeholders(item, data) for item in array]

    @staticmethod
    def handle_placeholders_in_string(value, data):
        return re.sub(r'#\{(\w+(\.\w+)*)\}', lambda match: YamlParser.get_nested_value(match.group(1), data), value)

    @staticmethod
    def get_nested_value(nested_key, data):
        keys = nested_key.split('.')
        current_data = data
        for key in keys:
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

