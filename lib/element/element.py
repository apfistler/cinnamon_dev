import os

from lib.base_content import BaseContent
from lib.site.site_type import SiteType

class Element(BaseContent):
    def __init__(self, site, element_type, full_path=None, key=None, site_type='user'):
        system_site_directory = site.config.get('system_site_directory')
        user_site_directory = site.config.get('user_site_directory')

        if full_path:
            # Extract the relative path from the full path
            base_site_directory = site.get(f'base_{site_type.value}_site_directory')

            # Determine the correct site directory based on site_type
            target_site_directory = system_site_directory if site_type == SiteType.SYSTEM else user_site_directory

            # Check if the relative path matches the target site directory
            if base_site_directory != target_site_directory:
                raise ValueError(f"The provided full_path '{full_path}' does not belong to the specified site_type '{site_type}'.")

            # Continue with your logic if the paths match
#            self.load(full_path)
            print(f"{site_type} -  Full path of {element_type} is {full_path}")
        else:
            # Handle the case where full_path is not provided
            pass

    def load(self, full_path):
        # Your load logic here
        print(f"Loading element from full path: {full_path}")


