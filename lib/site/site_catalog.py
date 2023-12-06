import os
from pprint import pprint

from lib.common import Common 
from lib.element.element import Element
from lib.site.site_location_type import SiteLocationType

class SiteCatalog:
    def __init__(self, site):
        self.site = site
        self.site_key = site.get('key')
        self.config = site.get('config')
        self.catalog(SiteLocationType.SYSTEM)

    def catalog(self, site_location_type):
        NON_SITE_ELEMENTS = ['metadata', 'data']

        site_structure = self.config.get('site_structure')

        if site_location_type == SiteLocationType.SYSTEM:
            site_directory = self.site.get('system_site_directory')
        elif site_location_type == SiteLocationType.USER:
            site_directory = self.site.get('user_site_directory')
        else: 
           print(f'SiteCatalog.catalog: Unknown site_location_type {site_location_type}')
           exit(1)

        metadata_directory = os.path.join(site_directory, Common.clean_path(site_structure['metadata']))

        for element_type, sub_directory in site_structure.items():
            element_type = element_type.lower()

            # Don't process metadata like any other project element
            if element_type in NON_SITE_ELEMENTS:
                continue

            element_directory = Element.get_element_path(self.site, site_location_type, element_type)

            # If Element Directory Does Not Exist that's OK
            if not os.path.exists(element_directory):
                continue

            file_dict = Common.get_files_recursively(element_directory)

            for full_path, d in file_dict.items():
                #print(f'{site_location_type}  -  {element_type}  - {full_path}')
                element = Element(self.site, element_type, site_location_type = site_location_type, full_path = full_path)

