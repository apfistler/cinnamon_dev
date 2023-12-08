#lib/site/site.py

import os

from lib.base_content import BaseContent
from lib.site.site_catalog import SiteCatalog
from lib.common import Common
from lib.metadata.metadata import Metadata

class Site(BaseContent):
    REQUIRED_FIELDS = ['name', 'url']
    
    def __init__(self, config, file_location_type, key):
        self.key = key 
        self.config = config
        self.file_location_type = file_location_type
        self.element_type = 'site'
        self.element_type_path = '.'

        self.metadata = Metadata(self, key=self.key)

        self.check_file_location_type()
        self.set_file_location_types()

        self.site_catalog = SiteCatalog(self)


    def get_site(self):
        return self

    def check_file_location_type(self):
        flt = self.config.get('file_location_types')

        if self.file_location_type not in flt:
            raise ValueError(f"File location type: {self.file_location_type} is unrecognized when invoking Site class.")

    def set_file_location_types(self):
        self.base_site_directory = {}
        self.site_directory = {} 
        file_location_types = self.config.get('file_location_types')

        for flt in file_location_types:
            self.base_site_directory[flt] = self.config.get(f'{flt}_site_directory')
            self.site_directory[flt] = os.path.join(self.base_site_directory[flt], self.key)

    def get_site_structure(self):
        REQUIRED_ELEMENTS = ['metadata', 'data', 'template', 'page', 'widget']
        site_structure = self.config.get('site_structure')

        missing_elements = [elem for elem in REQUIRED_ELEMENTS if elem not in site_structure]
        if missing_elements:
            raise ValueError(f"Missing required elements in configuration site_structure: {missing_elements}")

        self.site_structure = site_structure
        return self.site_structure 

    def get_element_directory(self, element_type):
        self.get_site_structure()
        return Common.clean_path(self.site_structure[element_type])

    def get_site_directory(self):
        self.set_file_location_types()
        return self.site_directory[self.file_location_type]

    def get_base_site_directory(self):
        return self.base_site_directory[self.file_location_type]

    def check_required_fields(self):
        super().check_required_fields()  # Call the base class method

