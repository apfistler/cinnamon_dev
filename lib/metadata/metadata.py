import os
import sys

from lib.base_content import BaseContent
from lib.metadata.metadata_parser import MetadataParser

class Metadata(BaseContent):
    REQUIRED_FIELDS = ['name']

    def __init__(self, metadata_id, metadata_path, data, site):
        # Merge attributes with merging logic
        self.merge_attributes(site.__dict__)

        # Create an instance of MetadataParser and parse placeholders in data
        metadata_parser = MetadataParser(data)
        self.metadata = metadata_parser.data

        super().__init__(metadata_id, metadata_path, self.metadata)

        # Look for CSS and JS files based on the 'id'
        self.check_required_fields()
        self.remove_duplicate_arrays()
        # Add any additional metadata-specific functionality here

    def merge_attributes(self, new_attributes):
        """
        Merge attributes with existing attributes.
        If an attribute is an array or a dictionary, merge them.
        If it's any other type, overwrite the existing value.
        """
        for key, value in new_attributes.items():
            if hasattr(self, key):
                current_value = getattr(self, key)

                # If the attribute is a dictionary, merge them
                if isinstance(current_value, dict) and isinstance(value, dict):
                    current_value.update(value)
                # If the attribute is a list, merge them
                elif isinstance(current_value, list) and isinstance(value, list):
                    current_value.extend(value)
                # For other types, overwrite the existing value
                else:
                    setattr(self, key, value)
            else:
                setattr(self, key, value)

    def to_dict(self):
        """
        Convert Metadata instance to a dictionary.
        """
        metadata_dict = super().to_dict()
        metadata_dict.update(vars(self))
        return metadata_dict

