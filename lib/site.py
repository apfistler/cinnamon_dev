import os
import yaml
import re

class Site:
    REQUIRED_FIELDS = ['id', 'name']

    def __init__(self, site_id, name, config):
        self.site_id = site_id
        self.name = name
        self.config = config
        self.parse()

    def __str__(self):
        return f"Site {self.site_id}: {self.name}"

    def parse(self):
        for key, value in self.config.items():
            self.config[key] = self._parse_property(value)

    def _parse_property(self, prop):
        if isinstance(prop, dict):
            return {k: self._parse_property(v) for k, v in prop.items()}
        elif isinstance(prop, list):
            return [self._parse_property(item) for item in prop]
        elif isinstance(prop, str):
            # Replace #{placeholder} with the value of the property
            prop = re.sub(r'#\{(\w+(\.\w+)*)\}', lambda match: self._get_nested_value(match.group(1)), prop)
            return prop
        else:
            return prop

    def _get_nested_value(self, nested_key):
        keys = nested_key.split('.')
        current_data = self.config
        for key in keys:
            if isinstance(current_data, dict) and key in current_data:
                current_data = current_data[key]
            elif isinstance(current_data, list) and key.isdigit() and 0 <= int(key) < len(current_data):
                current_data = current_data[int(key)]
            else:
                return f"Value for '{nested_key}' not found"
        return current_data

    def display_all(self):
        for key, value in self.config.items():
            print(f"{key}:")
            self._display_property(value, indent=2)

    def _display_property(self, prop, indent):
        if isinstance(prop, dict):
            for sub_key, sub_value in prop.items():
                print(f"{' ' * indent}{sub_key}:")
                self._display_property(sub_value, indent + 2)
        elif isinstance(prop, list):
            for idx, item in enumerate(prop):
                print(f"{' ' * indent}- ({idx}):")
                self._display_property(item, indent + 2)
        else:
            print(f"{' ' * indent}{prop}")

    def get(self, property_name):
        return self._get_nested_value(property_name)

    def set(self, property_name, value):
        keys = property_name.split('.')
        current_data = self.config
        for key in keys[:-1]:
            if isinstance(current_data, dict) and key in current_data:
                current_data = current_data[key]
            elif isinstance(current_data, list) and key.isdigit() and 0 <= int(key) < len(current_data):
                current_data = current_data[int(key)]
            else:
                return f"Invalid property path '{property_name}'"
        
        last_key = keys[-1]
        if isinstance(current_data, dict):
            current_data[last_key] = value
        elif isinstance(current_data, list) and last_key.isdigit() and 0 <= int(last_key) < len(current_data):
            current_data[int(last_key)] = value
        else:
            return f"Invalid property path '{property_name}'"

    @classmethod
    def from_yaml(cls, site_id, yaml_path):
        with open(yaml_path, 'r') as file:
            config = yaml.safe_load(file)
        name = config.get('name', 'Unknown')
        return cls(site_id, name, config)

