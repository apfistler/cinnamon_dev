import os
from pprint import pprint

from lib.common import Common 
from lib.element.element import Element

class SiteCatalog:
    def __init__(self, site):
        self.site = site
        self.site_key = site.get('key')
        self.config = site.get('config')
        self.catalog = {}

        flt = 'system'

        self.catalog_site_files(flt)

    def reset_attributes(self):
        self.file_location_type = None
        self.site_structure = None
        self.site_directory = None
        self.base_site_directory = None
        self.catalog_filename = None

    def get_attributes_as_dict(self):
        return {
            'file_location_type': self.file_location_type,
            'site_structure': self.site_structure,
            'site_directory': self.site_directory,
            'base_site_directory': self.base_site_directory,
            'catalog_filename': self.catalog_filename
        }

    def set_attributes_by_file_location_type(self, file_location_type):
        self.reset_attributes()

        catalog_filename = 'catalog.yaml'

        self.file_location_type = file_location_type
        self.site_structure = self.config.get('site_structure')
        self.check_site_structure()

        self.site_directory = self.site.get('site_directory')[self.file_location_type]
        self.base_site_directory = self.site.get('base_site_directory')[self.file_location_type]
        self.catalog_filename = os.path.join(self.site_directory, self.site_structure['data'], catalog_filename) 

        return self.get_attributes_as_dict()

    def check_site_structure(self):
        REQUIRED_ELEMENTS = ['metadata', 'data', 'template', 'page', 'widget']
        self.site_structure = self.config.get('site_structure')

        missing_elements = [elem for elem in REQUIRED_ELEMENTS if elem not in self.site_structure]
        if missing_elements:
            raise ValueError(f"Missing required elements in configuration site_structure: {missing_elements}")
       
    def get_element_directory(self, element_type):
        return Common.clean_path(self.site_structure[element_type]) 

    def read(self, file_location_type):
         # Make sure attributes are set
         self.set_attributes_by_file_location_type(file_location_type)

         if not Common.file_exists(self.catalog_filename):
             return

         self.catalog = YamlParser.parse_yaml(self.catalog_filename)

    def get_catalog_item(self, file_location_type, key):
        default_item = {
            'key': None,
            'checksum': None,
            'modified': False
        }

        return self.catalog.get(file_location_type, {}).get(key, default_item)

    def set_catalog_item(self, file_location_type, key, value):
        if file_location_type not in self.catalog:
            self.catalog[file_location_type] = {}

        self.catalog[file_location_type][key] = value


    def catalog_site_files(self, file_location_type):
        NON_SITE_ELEMENTS = ['metadata', 'data']

        self.set_attributes_by_file_location_type(file_location_type)
        metadata_directory = os.path.join(self.site_directory, self.get_element_directory('metadata'))

        for element_type, sub_directory in self.site_structure.items():
            element_type = element_type.lower()

            # Don't process metadata like any other project element
            if element_type in NON_SITE_ELEMENTS:
                continue

            element_directory = Element.get_element_path(self.site, file_location_type, element_type)

            # If Element Directory Does Not Exist that's OK
            if not os.path.exists(element_directory):
                continue

            file_dict = Common.get_files_recursively(element_directory)

            for full_path, d in file_dict.items():
                element = Element(self.site, element_type, file_location_type=file_location_type, full_path=full_path)
                key = element.get('key')

                item = self.get_catalog_item(file_location_type, key)
                catalog_checksum = item['checksum']
                current_checksum = Common.calculate_checksum(full_path)

                modified = catalog_checksum is not current_checksum

                item = {
                    'key': key,
                    'checksum': current_checksum,
                    'modified': modified
                }

                self.set_catalog_item(file_location_type, key, item)

