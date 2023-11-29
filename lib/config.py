import os
import yaml
import re
from .yaml_parser import YamlParser

class Config:
    REQUIRED_FIELDS = ['cinnamon_dir', 'config_dir', 'site_config_dir', 'site_dir', 'user_dir', 'user_config_dir', 'user_site_dir', 'user_site_config_dir', 'input_dir', 'output_dir']

    def __init__(self):
        self.data = {}
        self.protected_keys = ['admin']  # Add more keys if needed
        self.initialize()

    def read_file(self, filepath, error_message):
        if os.path.isfile(filepath):
            config_data = YamlParser.parse_yaml(filepath)
            if config_data:
                self.data.update(config_data)
        else:
            print(f"Error: {error_message}")
            exit(1)

    def read_system_config(self):
        system_config_path = '/etc/cinnamon.yaml'
        error_message = "Cinnamon has not been configured on this system."
        self.read_file(system_config_path, error_message)

    def read_defaults(self):
        defaults_path = os.path.join(self.data.get('config_dir', ''), 'defaults.yaml')
        self.read_file(defaults_path, "Error: Defaults file not found.")

    def read_user_config(self):
        home_dir = os.path.expanduser("~")
        user_config_path = os.path.join(home_dir, '.cinnamon.yaml')
        error_message = "Your user account has not been configured for use with Cinnamon. Please contact an administrator for access."
        self.read_file(user_config_path, error_message)

    def display_admins(self):
        admins = self.data.get('admin', {})
        for label, admin_info in admins.items():
            print(f"Admin: {label}\nFull Name: {admin_info['fullname']}\nEmail: {admin_info['email']}\n")

    def display_all(self):
        for key, value in self.data.items():
            print(f"{key}:")
            YamlParser.display_property(value, indent=2)

    def get(self, property_name):
        return YamlParser.get_nested_value(property_name, self.data)

    def set(self, property_name, value):
        keys = property_name.split('.')
        current_data = self.data
        for key in keys[:-1]:
            if isinstance(current_data, dict) and key in current_data:
                current_data = current_data[key]
            elif isinstance(current_data, list) and key.isdigit() and 0 <= int(key) < len(current_data):
                current_data = current_data[int(key)]
            else:
                print(f"Error: Invalid property path '{property_name}'")
                exit(1)
        
        last_key = keys[-1]
        if isinstance(current_data, dict):
            current_data[last_key] = value
        elif isinstance(current_data, list) and last_key.isdigit() and 0 <= int(last_key) < len(current_data):
            current_data[int(last_key)] = value
        else:
            print(f"Error: Invalid property path '{property_name}'")
            exit(1)

    def initialize(self):
        self.read_system_config()

        # Parse the configuration after reading the system config
        self.parse()

        # Read the defaults file and update the configuration
        self.read_defaults()

        # Read the user config after reading the defaults
        self.read_user_config()
        self.parse()

    def parse(self):
        YamlParser.parse_properties(self.data, self.data)

    def check_required_fields(self):
        for field in self.REQUIRED_FIELDS:
            if field not in self.data:
                print(f"Error: Required field '{field}' is missing. Please check your configuration.")
                exit(1)

# Usage Example for Reference:
# Create an instance of the Config class
#config = Config()

# Check and initialize the configuration
#config.check_required_fields()

# Display information about administrators from the configuration
#config.display_admins()

# Display all properties in the configuration
#print("\nAll Configuration Properties:")
#config.display_all()

# Get the value of a specific property
#cinnamon_dir_value = config.get('cinnamon_dir')
#print(f"\nValue of 'cinnamon_dir': {cinnamon_dir_value}")

# Set the value of a specific property
#config.set('new_property', 'new_value')

# Display all properties after setting a new one
#print("\nAll Configuration Properties after setting 'new_property':")
#config.display_all()
