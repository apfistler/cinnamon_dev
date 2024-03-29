#/lib/page/page_metadta

import os
import sys

from lib.base_content import BaseContent
from lib.page.page_metadata_parser import PageMetadataParser

class Page_Metadata(BaseContent):
    REQUIRED_FIELDS = ['name']

    def __init__(self, page_metadata_id, page_metadata_path, data, site):
        # Merge attributes with merging logic
        self.merge_attributes(site.__dict__)

        # Create an instance of PageMetadataParser and parse placeholders in data
        page_metadata_parser = PageMetadataParser(data)
        self.metadata = page_metadata_parser.data

        super().__init__(page_metadata_id, page_metadata_path, self.metadata)

        # Look for CSS and JS files based on the 'id'
        self.load_assets()

        self.check_required_fields()
        self.remove_duplicate_arrays()
        # Add any additional page_metadata-specific functionality here

    def merge_attributes(self, new_attributes):
        """
        Merge attributes with existing attributes.
        If an attribute is an array or a dictionary, merge them.
        If it's any other type, overwrite the existing value.
        """
        for key, value in new_attributes.items():
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


    def load_assets(self):
        """
        Look for CSS and JS files based on the 'id' and add them to the 'css' and 'js' arrays.
        """
        # Convert '.' to '/' in the 'id'
        id_path = self.id.replace('.', '/')

        # Look for CSS and JS files in the site directory
        site_dir = self.site_dir
        css_path = os.path.join(site_dir, 'css', f"{id_path}.css")
        js_path = os.path.join(site_dir, 'js', f"{id_path}.js")

        # Check if CSS file exists and append to the 'css' array
        if os.path.isfile(css_path):
            self.css.append(f"/css/{id_path}.css")

        # Check if JS file exists and append to the 'js' array
        if os.path.isfile(js_path):
            self.js.append(f"/js/{id_path}.js")

    def has_attr(self, param):
         return hasattr(self, param) and getattr(self, param) is not None


    def to_dict(self):
        """
        Convert Page_Metadata instance to a dictionary.
        """
        return vars(self)
