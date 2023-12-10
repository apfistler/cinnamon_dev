#lib/site/site.py

import os
import yaml
import atexit
from datetime import datetime

from lib.base_content import BaseContent
from lib.site.site_catalog import SiteCatalog
from lib.common import Common
from lib.metadata.metadata import Metadata
from lib.yaml_parser import YamlParser

class Site(BaseContent):
    REQUIRED_FIELDS = ['name', 'url']
    
    def __init__(self, config, file_location_type, key):
        self.key = key 
        self.config = config
        self.file_location_type = file_location_type
        self.element_type = 'site'
        self.element_type_path = '.'

        self.keep_lock_file = False
        self.lock_file_path = os.path.join(self.get_site_directory(), self.get_element_directory('data'), 'lockfile')

        self.lockfile_exists_with_error()

        self.create_lock_file()

        self.metadata = self.get_metadata()
        self.check_file_location_type()
        self.set_file_location_types()

        self.site_catalog = SiteCatalog(self)
        atexit.register(self.remove_lock_file)

    def __del__(self):
        self.remove_lock_file()

    def get_site(self):
        return self

    def get_metadata(self):
        metadata_key = os.path.join(self.get_element_directory('metadata'), 'metadata.yaml')
        metadata = Metadata(self, key=metadata_key)

        return metadata.self

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

    def lockfile_exists_with_error(self):
        if self.lockfile_exists(): 
            self.keep_lock_file = True

            yaml = YamlParser.parse_yaml(self.lock_file_path)
            #lock_datetime = datetime.strptime(yaml['datetime'], '%Y-%m-%d %H:%M:%S.%f')
            total_seconds = int((datetime.now() - yaml['datetime']).total_seconds())
            s = 's' if total_seconds != 1 else ''  # Adjusted the variable name

            print(f"Site: {self.key} has been temporarily locked by {yaml['username']} ({yaml['fullname']} - {yaml['email']}) at {yaml['datetime']} ({total_seconds} second{s} ago).")

            if total_seconds > 500:
                print(f"You may safely remove {self.lock_file_path} and try again.")

            exit(1)
        else:
            return False

    def lockfile_exists(self):
        return os.path.exists(self.lock_file_path)


    def create_lock_file(self):
        lock_data = {
            'status': 'locked',
            'username': self.config.get('username'),
            'fullname': self.config.get('fullname'),
            'email': self.config.get('email'),
            'datetime': datetime.now()
        }

        lock_str = yaml.dump(lock_data)

        with open(self.lock_file_path, 'w') as lock_file:
            lock_file.write(lock_str)

    def remove_lock_file(self):
        if self.keep_lock_file:
            return

        if self.lockfile_exists():
            os.remove(self.lock_file_path)

