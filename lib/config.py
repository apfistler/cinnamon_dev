import os
import yaml
import re

class Config:
    REQUIRED_FIELDS = ['cinnamon_dir', 'config_dir', 'sites_dir', 'user_dir', 'user_config_dir', 'user_sites_dir', 'input_dir', 'output_dir']

    def __init__(self):
        self.data = {}
        self.protected_keys = ['admin']  # Add more keys if needed
        self.initialize()

    def read_file(self, filepath, error_message):
        if os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                config_data = yaml.safe_load(file)
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
            self._display_property(value, indent=2)

    def _display_property(self, prop, indent):
        if isinstance(prop, dict):
            for sub_key, sub_value in prop.items():
                print(f"{' ' * indent}{sub_key}:")
                self._display_property(sub_value, indent + 2)
        elif isinstance(prop, list):
            for item in prop:
                print(f"{' ' * indent}-")
                self._display_property(item, indent + 2)
        else:
            print(f"{' ' * indent}{prop}")

    def get(self, property_name):
        return self.data.get(property_name)

    def set(self, property_name, value):
        self.data[property_name] = value

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
        for key, value in self.data.items():
            self.data[key] = self._parse_property(value)

    def _parse_property(self, prop):
        if isinstance(prop, dict):
            return {k: self._parse_property(v) for k, v in prop.items()}
        elif isinstance(prop, list):
            return [self._parse_property(item) for item in prop]
        elif isinstance(prop, str):
            # Replace #{property_name} with the value of the property
            prop = re.sub(r'#\{(\w+)\}', lambda match: str(self.data.get(match.group(1), match.group(0))), prop)
            # Replace ${environmental_variable} with the value of the environmental variable
            prop = re.sub(r'\$\{(\w+)\}', lambda match: str(os.environ.get(match.group(1), match.group(0))), prop)
            return prop
        else:
            return prop

    def check_required_fields(self):
        for field in self.REQUIRED_FIELDS:
            if field not in self.data:
                print(f"Error: Required field '{field}' is missing. Please check your configuration.")
                exit(1)
