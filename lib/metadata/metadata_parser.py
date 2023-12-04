import re

class MetadataParser:
    def __init__(self, data):
        if not isinstance(data, dict):
            raise ValueError("Input data must be a dictionary.")
        
        self.data = data
        self.replace_placeholders(self.data)  # Rename method for clarity

    def replace_placeholders(self, data):
        for key, value in data.items():
            data[key] = self.handle_placeholders(value)

    def handle_placeholders(self, value):
        if isinstance(value, dict):
            return {k: self.handle_placeholders(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [self.handle_placeholders(item) for item in value]
        elif isinstance(value, str):
            return self.handle_placeholders_in_string(value)
        else:
            return value

    def handle_placeholders_in_string(self, value):
        return re.sub(r'#\{(\w+(\.\w+)*)\}', lambda match: self.get_nested_value(match.group(1)), value)

    def get_nested_value(self, nested_key):
        keys = nested_key.split('.')
        current_data = self.data
        for key in keys:
            if isinstance(current_data, dict) and key in current_data:
                current_data = current_data[key]
            elif isinstance(current_data, list) and key.isdigit() and 0 <= int(key) < len(current_data):
                current_data = current_data[int(key)]
            else:
                raise KeyError(f"Value for '{nested_key}' not found")
        return current_data

