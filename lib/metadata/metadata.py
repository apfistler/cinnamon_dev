import os
import sys

from lib.base_content import BaseContent
from lib.metadata.metadata_parser import MetadataParser
from lib.common import Common
from lib.yaml_parser import YamlParser
from pprint import pprint

class Metadata(BaseContent):

    def __init__(self, element, key=None, path=None):
        self.element = element
        self.site = self.element.get('site')
        self.config = self.site.get('config')
        self.site_location_type = element.get('site_location_type')
        self.base_system_site_directory = element.get('base_system_site_directory')
        self.base_user_site_directory = element.get('base_user_site_directory')
        self.base_site_directory = element.get(f'base_{self.site_location_type.value}_site_directory')
        self.site_directory = self.element.get(f'site_directory')
        self.element_type = self.element.get('element_type')
        self.element_type_path = self.element.get('element_type_path')

        print(f'MD Site Location Type: {self.site_location_type.value}')
        print(f'MD Base System Site Directory: {self.base_system_site_directory}')
        print(f'MD Base User Site Directory: {self.base_system_site_directory}')
        print(f'MD Site Directory: {self.site_directory}')
        print(f"MD Key: {key}")
        print(f"MD Path: {path}")

        if not (key or path):
            raise ValueError("Either key or path must be supplied to the metadata class.")

        if key:
            self.key = key
            self.path = os.path.join(self.site_directory, self.key)
        elif path:
            self.key = os.relpath(path, self.site_directory)
            self.path = path

        if not Common.file_exists(self.path):
            raise ValueError("Metadata file: {path} does not exist when instantiating Metadata class.")


        if not Common.file_exists(self.path):
            raise ValueError("Metadata file #{self.path} cannot be located.")

        self.read()
        self.apply_cascading()

    def read_cascading(self):
        if not hasattr(self, 'element_params'):
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
        if not hasattr(self, 'element_params'):
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
        collective_params_dict = Common.merge_dicts(*dicts, self.element_params.to_dict())
        self.collective_params = self.Param(collective_params_dict)

    def read(self):
        dictionary = YamlParser.parse_yaml(self.path)
        self.element_params = self.Param(dictionary)

    def write(self):
        yaml_content = yaml.dump(self.element_params.to_dict(), default_flow_style=False)

        with open(self.path, 'w') as file:
            file.write(yaml_content)

    def set_param(self, param, value):
        self.element_params.set(param, value)

    def get_param(self, param):
        return self.element_params.get(param)

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
            self._params[key] = value

        def get(self, key):
            return self._params.get(key, None)

