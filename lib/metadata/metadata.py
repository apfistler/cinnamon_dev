import os
import sys

from lib.base_content import BaseContent
from lib.metadata.metadata_parser import MetadataParser
from lib.common import Common
from lib.yaml_parser import YamlParser

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

        if not (key or path):
            raise ValueError("Either key or path must be supplied to the metadata class.")

        print(f'MD Site Location Type: {self.site_location_type.value}')
        print(f'MD Base System Site Directory: {self.base_system_site_directory}')
        print(f'MD Base User Site Directory: {self.base_system_site_directory}')
        print(f'MD Site Directory: {self.site_directory}')

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

        self.apply_cascading()

    def apply_cascading(self):
        site_structure = self.config.get('site_structure')
        metadata_subdir = site_structure['metadata']
        metadata_filename = self.config.get('metadata_filename')

        directory = os.path.join(self.site_directory, metadata_subdir, self.element_type_path)
        files = Common.find_files_by_name(directory, metadata_filename)
        files.append(self.path)

        dicts = []
        for file in files:
            dicts.append(YamlParser.parse_yaml(file))

        self.param = self.Param(dicts)

        print(self.param.to_dict())

    class Param:
        def __init__(self, dicts):
            for d in dicts:
                for key, value in d.items():
                    setattr(self, key, value)

        def to_dict(self):
            return {key: getattr(self, key) for key in dir(self) if not key.startswith('__') and not callable(getattr(self, key))}

