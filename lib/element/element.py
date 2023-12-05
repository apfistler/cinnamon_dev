import os

from lib.base_content import BaseContent
from lib.site.site_location import SiteLocation
from lib.common import Common


class Element(BaseContent):
    def __init__(self, site, element_type, full_path=None, key=None, site_location=SiteLocation.USER):
        self.element_type = element_type.lower()  # Fix here
        self.site = site
        self.site_location = site_location

        config = self.site.get('config')
        self.config = config
        self.site_structure = config.get('site_structure')

        if element_type not in self.site_structure.keys():
            raise ValueError(f"Error: Element type '{element_type}' is not valid in the site structure.")

        self.base_system_site_directory = site.get('base_system_site_directory')
        self.base_user_site_directory = site.get('base_user_site_directory')
        self.base_site_directory = site.get(f'base_{site_location.value}_site_directory')
        self.site_directory = site.get(f'{site_location.value}_site_directory')

        if full_path:
            # Determine the correct site directory based on site_location
            target_site_directory = self.base_system_site_directory if site_location == SiteLocation.SYSTEM else self.base_user_site_directory

            # Check if the relative path matches the target site directory
            if self.base_site_directory != target_site_directory:
                raise ValueError(f"The provided full_path '{full_path}' does not belong to the specified site_location '{site_location}'.")
        else:
            full_path = self.find_by_key(key)

        if not Common.file_exists(full_path):
            raise ValueError(f"Element {element_type} does not exist in '{full_path}'")

        self.path = full_path
        self.key = os.path.relpath(self.path, start=self.site_directory)

        print(f"Element type: {self.element_type}")
        print(f"Site Location: {self.site_location}")
        print(f"Key: {self.key}")
        print(f"Path: {self.path}")

        self.metadata_path = self.get_metadata_path()
        print(f'Metadata path: {self.metadata_path}')
        

    def find_path_by_key(self, key):
        path = self._get_element_path(self.element_type)

        return Common.find_files_by_partial_name(path, key)[0]

    def get_metadata_path(self):
        name = f"{os.path.splitext(self.key)[0]}.yaml"
        metadata_path = self._get_element_path('metadata')
        return os.path.join(metadata_path, name)

    @staticmethod
    def get_element_path(site, site_location, element_type):
        config = site.get('config')
        site_structure = config.get('site_structure')
        sub_directory = Common.clean_path(site_structure[element_type])

        site_directory = site.get(f'{site_location.value}_site_directory')
        return os.path.join(site_directory, sub_directory)

    def _get_element_path(self, element_type):
        return Element.get_element_path(self.site, self.site_location, element_type)

