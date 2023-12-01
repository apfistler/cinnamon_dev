#;on/base_content.py

from lib.yaml_parser import YamlParser

class BaseContent:
    REQUIRED_FIELDS = []

    def __init__(self, content_id, content_path, metadata):
        self.id = content_id
        self.path = content_path
        self.metadata = metadata
        self._merge_metadata()
        self.check_required_fields()

    def _merge_metadata(self):
        # Merge metadata values into the instance properties
        for key, value in self.metadata.items():
            current_value = getattr(self, key, None)

            # If the attribute is a dictionary, merge them
            if isinstance(current_value, dict) and isinstance(value, dict):
                current_value.update(value)
            # If the attribute is a list, merge them
            elif isinstance(current_value, list) and isinstance(value, list):
                current_value.extend(value)
            # For other types, overwrite the existing value
            else:
                setattr(self, key, value)

    def display_all(self):
        # Display all properties in the content (both site and page)
        print(f"\nAll Properties for {self.__class__.__name__} '{self.id}':")
        self._display_property(self.__dict__, indent=2)

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
        # Get the value of a specific property
        return getattr(self, property_name, None)

    def set(self, property_name, value):
        # Set the value of a specific property
        setattr(self, property_name, value)

    def check_required_fields(self):
        for field in self.REQUIRED_FIELDS:
            if field not in self.metadata:
                print(f"Error: Required field '{field}' is missing in {self.__class__.__name__} '{self.id}'.")
                exit(1)

    def remove_duplicate_arrays(self):
        """
        Remove duplicates from arrays in the instance properties.
        """
        for key, value in self.__dict__.items():
            if isinstance(value, list):
                # Remove duplicates from the list
                setattr(self, key, list(set(value)))
