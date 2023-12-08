import os
import sys

from lib.base_content import BaseContent
from lib.common import Common
from lib.yaml_parser import YamlParser

class Metadata(BaseContent):

    def __init__(self, element, key=None, path=None):
        self.element = element
        self.site = self.element.get_site()
        self.config = self.site.get('config')

        self.site_directory = self.site.get_site_directory()
        self.element_type = self.element.get('element_type')
        self.element_type_path = self.element.get('element_type_path')

#        print(f'MD Site Location Type: {self.file_location_type}')
#        print(f'MD Site Directory: {self.site_directory}')
#        print(f"MD Key: {key}")
#        print(f"MD Path: {path}")

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

        self.read()
        self.apply_cascading()

    def read_cascading(self):
        if not hasattr(self, 'self'):
            self.read()

        site_structure = self.config.get('site_structure')
        metadata_subdir = site_structure['metadata']
        metadata_filename = self.config.get('metadata_filename')

        directory = os.path.join(self.site_directory, metadata_subdir, self.element_type_path)
        files = Common.find_files_by_name(directory, metadata_filename)

        dicts = []
        for file in files:
            dicts.append(YamlParser.parse_yaml(file))

        return dicts

    def apply_cascading(self):
        if not hasattr(self, 'self'):
            self.read()

        site_structure = self.config.get('site_structure')
        metadata_subdir = site_structure['metadata']
        metadata_filename = self.config.get('metadata_filename')

        directory = os.path.join(self.site_directory, metadata_subdir, self.element_type_path)
        files = Common.find_files_by_name(directory, metadata_filename)

        dicts = []
        for file in files:
            file_dict = YamlParser.parse_yaml(file)
            if file_dict:  # Check if the parsing was successful
                #del file_dict['key']
                dicts.append(file_dict)

        if not dicts:  # Check if dicts is still empty
            return

        # Merge the list of dictionaries using Common.merge_dicts
        all_dict = Common.merge_dicts(*dicts, self.self.to_dict())
        self.all = self.Param(all_dict)

    def read(self):
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

