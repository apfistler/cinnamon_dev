#lib/site/site.py

import os

from lib.base_content import BaseContent
from lib.site.site_catalog import SiteCatalog

class Site(BaseContent):
    REQUIRED_FIELDS = ['name', 'url']
    
    def __init__(self, config, key):
        self.key = key 
        self.config = config
        self.base_system_site_directory = config.get('system_site_directory')
        self.base_user_site_directory = config.get('user_site_directory')
        self.system_site_directory = os.path.join(self.base_system_site_directory, key)
        self.user_site_directory = os.path.join(self.base_user_site_directory, key)

        system_site_catalog = SiteCatalog(self)


        #super().__init__(site_id, site_path, data)
        # Add any additional site-specific functionality here
        #self.site_dir = site_path

        #self.check_required_fields()

        # Add any additional obj_metadata-specific functionality here

    def check_required_fields(self):
        super().check_required_fields()  # Call the base class method

