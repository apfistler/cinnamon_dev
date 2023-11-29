from .yaml_parser import YamlParser

class Site:
    REQUIRED_FIELDS = ['id', 'name']

    def __init__(self, site_id, config):
        self.site_id = site_id
        self.config = config
        self.parse()

    def parse(self):
        # Parse the configuration using the YamlParser
        YamlParser.parse_properties(self.config, self.config)

        # Validate required fields
        YamlParser.validate_required_fields(self.config, self.REQUIRED_FIELDS)

    def display_all(self):
        # Display all properties in the site configuration
        print(f"\nAll Properties for Site '{self.site_id}':")
        self._display_property(self.config, indent=2)

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
        # Get the value of a specific property in the site configuration
        return YamlParser.get_nested_value(property_name, self.config)

    def set(self, property_name, value):
        # Set the value of a specific property in the site configuration
        keys = property_name.split('.')
        current_data = self.config
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


# Commented-out Usage Statement
"""
# Example Usage of the Site class

# Create a sample site configuration
site_config = {
    'id': 'sample_site',
    'name': 'Sample Site',
    'settings': {
        'theme': 'default',
        'language': 'en',
        'timezone': 'UTC',
    },
    'pages': [
        {'title': 'Home', 'url': '/home'},
        {'title': 'About', 'url': '/about'},
    ],
}

# Create an instance of the Site class
sample_site = Site(site_id='sample_site', name='Sample Site', config=site_config)

# Display all properties in the site configuration
sample_site.display_all()

# Get the value of a specific property in the site configuration
theme_value = sample_site.get('settings.theme')
print(f"\nValue of 'settings.theme': {theme_value}")

# Set the value of a specific property in the site configuration
sample_site.set('settings.language', 'fr')

# Display all properties after setting a new one
print("\nAll Properties after setting 'settings.language':")
sample_site.display_all()
"""

