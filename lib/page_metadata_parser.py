import re

class PageMetadataParser:
    def __init__(self, data):
        self.data = data
        self.parse(self.data)  # Parse placeholders at initialization

    def parse(self, data):
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
                return f"Value for '{nested_key}' not found"
        return current_data

