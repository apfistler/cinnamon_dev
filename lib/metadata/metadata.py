import os
import sys

from lib.base_content import BaseContent
from lib.common import Common
from lib.yaml_parser import YamlParser
from pprint import pprint

class Metadata(BaseContent):

    def __init__(self, element, key=None, path=None):
        self.element = element
        self.site = self.element.get_site()
        self.config = self.site.get('config')

        self.site_directory = self.site.get_site_directory()
        self.element_type = self.element.get('element_type')
        self.element_type_path = self.element.get('element_type_path')

        if not (key or path):
            raise ValueError("Either key or path must be supplied to the metadata class.")

        if key:
            self.key = key
            self.path = os.path.join(self.site.get_site_directory(), self.key)
        elif path:
            self.key = os.relpath(path, self.site_directory)
            self.path = path

#        if not Common.file_exists(self.path):
#            raise ValueError("Metadata file: {path} does not exist when instantiating Metadata class.")

#        print(f'MD Site Directory: {self.site.get_site_directory()}')
#        print(f"MD Key: {self.key}")
#        print(f"MD Path: {self.path}")

        self.read()

#        if self.element_type != 'site':
        self.apply_cascading()

    def apply_cascading(self):
        if self.element_type == 'site':
            return

        if not hasattr(self, 'self'):
            self.read()

        site_structure = self.config.get('site_structure')
        metadata_subdir = site_structure['metadata']
        metadata_filename = self.config.get('metadata_filename')

        directory = os.path.join(self.site_directory, metadata_subdir, self.element_type_path)
        files = Common.find_files_by_name(directory, metadata_filename)

        depth_limit = len(os.path.normpath(self.path).split(os.path.sep))

        dicts = []
        for file in files:
            # Get the depth of the current file
            file_depth = len(os.path.normpath(file).split(os.path.sep))
    
            # Check if the depth exceeds the limit
            if file_depth > depth_limit:
                break 

            file_dict = YamlParser.parse_yaml(file)
            if file_dict:  # Check if the parsing was successful
                #del file_dict['key']
                dicts.append(file_dict)

        if not dicts:  # Check if dicts is still empty
            return

        # Merge the list of dictionaries using Common.merge_dicts
        all_dict = Common.merge_dicts(*dicts, self.self.to_dict())
        self.all = self.Param(all_dict)

        site_md = self.site.get_metadata()
        self.all = self._merge_site_metadata(self.all)
        

        pprint(self.all.to_dict())
         

    def _merge_site_metadata(self, metadata):
        site_metadata = self.site.get_metadata()
        metadata.merge(site_metadata)

        return metadata

    def read(self):
        print(f"PATH is {self.path}")
        if Common.file_exists(self.path):
            dictionary = YamlParser.parse_yaml(self.path)
        else:
            dictionary = {}

        self.self = self.Param(dictionary)

    def write(self):
        yaml_content = yaml.dump(self.self.to_dict(), default_flow_style=False)

        with open(self.path, 'w') as file:
            file.write(yaml_content)

    def set_param(self, param, value):
        self.self.set(param, value)

    def get_param(self, param):
        return self.self.get(param)

    class Param:
        def __init__(self, dictionary):
            if isinstance(dictionary, dict):
                for key, value in dictionary.items():
                    setattr(self, key, value)

        def to_dict(self):
            result = {}
            for key, value in self.__dict__.items():
                if isinstance(value, Metadata.Param):
                    result[key] = value.to_dict()
                else:
                    result[key] = value

            return result

        def set(self, key, value):
            setattr(self, key, value)

        def get(self, key, default=None):
            return getattr(self, key, default)

        def merge(self, other_param):
            if not isinstance(other_param, Metadata.Param):
                raise ValueError("Merge can only be performed with another Param instance.")

            for key, value in other_param.__dict__.items():
                self.set(key, value)
