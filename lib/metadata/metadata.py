import os
import sys

from lib.base_content import BaseContent
from lib.metadata.metadata_parser import MetadataParser
from lib.common import Common

class Metadata(BaseContent):

    def __init__(self, element, key=None, path=None):
        self.element = element
        self.site = self.element.get('site')
        self.config = self.site.get('config')
        self.site_location_type = element.get('site_location_type')
        self.base_system_site_directory = element.get('base_system_site_directory')
        self.base_user_site_directory = element.get('base_user_site_directory')
        self.base_site_directory = element.get(f'base_{self.site_location_type.value}_site_directory')
        self.site_directory = self.element.get(f'site_directory')
        self.element_type = self.element.get('element_type')
        self.element_type_path = self.element.get('element_type_path')

        if not (key or path):
            raise ValueError("Either key or path must be supplied to the metadata class.")

        print(f'MD Site Location Type: {self.site_location_type.value}')
        print(f'MD Base System Site Directory: {self.base_system_site_directory}')
        print(f'MD Base User Site Directory: {self.base_system_site_directory}')
        print(f'MD Site Directory: {self.site_directory}')

        if key:
            self.key = key
            self.path = os.path.join(self.site_directory, self.key)

        if not Common.file_exists(self.path):
            raise ValueError("Metadata file #{self.path} cannot be located.")

        self.apply_cascading()

    def apply_cascading(self):
        site_structure = self.config.get('site_structure')
        metadata_subdir = site_structure['metadata']

        metadata_filename = 'metadata.yaml'

        directory = os.path.join(self.site_directory, metadata_subdir, self.element_type_path)

        print(f"MD ETP {directory}")
        files = Common.find_files_by_name(directory, metadata_filename)
        print(f'MD FILES {files}')

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

