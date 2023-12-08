import os

from lib.base_content import BaseContent
from lib.metadata.metadata import Metadata
from lib.common import Common


class Element(BaseContent):
    def __init__(self, site, element_type, full_path=None, key=None):
        self.element_type = element_type.lower() 
        self.site = site
        self.file_location_type = site.get('file_location_type')

        config = self.site.get('config')
        self.config = config
        self.site_structure = config.get('site_structure')

        if element_type not in self.site_structure.keys():
            raise ValueError(f"Error: Element type '{element_type}' is not valid in the site structure.")
        
        self.element_type_path = self.site_structure[element_type]

        self.base_site_directory = site.get('base_site_directory')[self.file_location_type]
        self.site_directory = site.get('site_directory')[self.file_location_type] 

        if full_path:
            # Determine the correct site directory based on file_location_type
            target_site_directory = self.site.get('base_site_directory')[self.file_location_type]

            # Check if the relative path matches the target site directory
            if self.base_site_directory != target_site_directory:
                raise ValueError(f"The provided full_path '{full_path}' does not belong to the specified file_location_type '{file_location_type}'.")
        else:
            full_path = self.find_by_key(key)

        if not Common.file_exists(full_path):
            raise ValueError(f"Element {element_type} does not exist in '{full_path}'")

        self.path = full_path
        self.key = os.path.relpath(self.path, start=self.site_directory)

        self.metadata_path = self.get_metadata_path()
        self.metadata_key = os.path.relpath(self.metadata_path, self.site_directory)

        self.metadata = Metadata(self, key=self.metadata_key)

    def find_path_by_key(self, key):
        path = self._get_element_path(self.element_type)

        return Common.find_files_by_partial_name(path, key)[0]

    def get_site(self):
        return self.site

    def get_filename(self):
        return os.path.basename(self.path)

    def get_metadata_path(self):
        name = f"{os.path.splitext(self.key)[0]}.yaml"
        metadata_path = self._get_element_path('metadata')
        
        return os.path.join(metadata_path, name)

    @staticmethod
    def get_element_path(site, file_location_type, element_type):
        config = site.get('config')
        site_structure = config.get('site_structure')
        sub_directory = Common.clean_path(site_structure[element_type])

        site_directory = site.get('site_directory')[file_location_type]
        return os.path.join(site_directory, sub_directory)

    def _get_element_path(self, element_type):
        return Element.get_element_path(self.site, self.file_location_type, element_type)

    def get_element_type_by_extension(self, extension):
        """
        Get the element type or label based on the given file extension.
        """
        for element_type, extensions in self.site_structure.items():
            if extension.lower() in extensions:
                return element_type

        # If the extension is not found in any element type, return None or a default value
        return 'file' 

