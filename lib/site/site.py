#lib/site/site.py

import os

from lib.base_content import BaseContent
from lib.site.site_catalog import SiteCatalog

class Site(BaseContent):
    REQUIRED_FIELDS = ['name', 'url']
    
    def __init__(self, config, key):
        self.key = key 
        self.config = config
        self.set_file_location_types()
        self.site_catalog = SiteCatalog(self)

    def set_file_location_types(self):
        self.base_site_directory = {}
        self.site_directory = {} 
        file_location_types = self.config.get('file_location_types')

        for flt in file_location_types:
            self.base_site_directory[flt] = self.config.get(f'{flt}_site_directory')
            self.site_directory[flt] = os.path.join(self.base_site_directory[flt], self.key)

    def check_required_fields(self):
        super().check_required_fields()  # Call the base class method

