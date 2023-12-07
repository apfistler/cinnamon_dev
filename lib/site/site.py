#lib/site/site.py

import os

from lib.base_content import BaseContent
from lib.site.site_catalog import SiteCatalog

class Site(BaseContent):
    REQUIRED_FIELDS = ['name', 'url']
    
    def __init__(self, config, file_location_type, key):
        self.key = key 
        self.config = config
        self.file_location_type = file_location_type

        self.check_file_location_type()
        self.set_file_location_types()

        self.site_catalog = SiteCatalog(self)

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

    def check_required_fields(self):
        super().check_required_fields()  # Call the base class method

