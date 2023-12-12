import os
import yaml
from pprint import pprint
from collections import defaultdict

from lib.common import Common 
from lib.element.element import Element
from lib.page.page import Page
from lib.yaml_parser import YamlParser

class SiteCatalog:
    def __init__(self, site, file_structure_type=None):
        self.site = site
        self.site_key = site.get('key')
        self.config = site.get('config')
        self.file_structure_type = file_structure_type or self.site.get('file_structure_type')
        self.catalog = {}

        self.build_catalog(self.file_structure_type)

    def reset_attributes(self):
        self.file_structure_type = None
        self.site_structure = None
        self.site_directory = None
        self.base_site_directory = None
        self.catalog_filename = None

    def get_attributes_as_dict(self):
        return {
            'file_structure_type': self.file_structure_type,
            'site_structure': self.site.get_site_structure(),
            'site_directory': self.site_directory,
            'base_site_directory': self.base_site_directory,
            'catalog_filename': self.catalog_filename
        }

    def set_attributes_by_file_structure_type(self, file_structure_type):
        self.reset_attributes()

        catalog_filename = 'catalog.yaml'

        self.file_structure_type = file_structure_type
        self.site_structure = self.site.get_site_structure() 

        self.site_directory = self.site.get('site_directory')[self.file_structure_type]
        self.base_site_directory = self.site.get('base_site_directory')[self.file_structure_type]

        data_directory = os.path.join(self.site_directory, self.site_structure['data'])
        Common.mkdir(data_directory)

        self.catalog_filename = os.path.join(data_directory, catalog_filename) 

        return self.get_attributes_as_dict()

    def read(self, file_structure_type):
         # Make sure attributes are set
         self.set_attributes_by_file_structure_type(file_structure_type)

         if not Common.file_exists(self.catalog_filename):
             return

         self.catalog = YamlParser.parse_yaml(self.catalog_filename)
         self.update_catalog_integrity(file_structure_type)

    def write(self, file_structure_type):
        self.set_attributes_by_file_structure_type(file_structure_type)
        self.update_catalog_integrity(file_structure_type)

        with open(self.catalog_filename, 'w') as file:
            yaml.dump(self.catalog, file, default_flow_style=False)


    def update_catalog_integrity(self, file_structure_type):
        catalog_items = self.catalog.get(file_structure_type, {})

        keys_to_purge = defaultdict(list)

        for element_type, element_dict in catalog_items.items():
            for key, catalog_item in element_dict.items():
                if full_path := catalog_item.get('path'):
                    if not Common.file_exists(full_path):
                        keys_to_purge[element_type].append(key)

        for element_type, keys in keys_to_purge.items():
            for key in keys:
                self.remove_catalog_item(file_structure_type, element_type, key)

    def get_catalog_item(self, file_structure_type, element_type, key):
        default_item = {
            'id': self.get_next_catalog_id(file_structure_type),
            'key': None,
            'filename': None,
            'path': None,
            'element_type': None,
            'metadata_filename': None,
            'checksum': None,
            'modified': False
        }

        return self.catalog.get(file_structure_type, {}).get(element_type, {}).get(key, default_item)

    def set_catalog_item(self, file_structure_type, element_type, key, value):
        if file_structure_type not in self.catalog:
            self.catalog[file_structure_type] = {}

        if element_type not in self.catalog[file_structure_type]:
            self.catalog[file_structure_type][element_type] = {}

        self.catalog[file_structure_type][element_type][key] = value

    def remove_catalog_item(self, file_structure_type, element_type, key):
        try:
            del self.catalog[file_structure_type][element_type][key]
        except KeyError:
            pass

    def get_next_catalog_id(self, file_structure_type):
        catalog_ids = []

        for element_type, catalog_item in self.catalog.get(file_structure_type, {}).items():
            for key, item in catalog_item.items():
                if item.get('id') is not None:
                    catalog_ids.append(item.get('id'))

        return max(catalog_ids, default=0) + 1

    def get_duplicate_elements(self, file_structure_type):
        catalog_items = self.catalog.get(file_structure_type)

        new_dict = {}
        filtered_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))

        for element_type, element_dict in catalog_items.items():
            if not new_dict.get(element_type):
                new_dict[element_type] = {}
 
            for key, catalog_item in element_dict.items():
                if full_path := catalog_item.get('path'):
                    path, filename = os.path.split(full_path)
                    base_name, extension = os.path.splitext(filename)

                    if not new_dict[element_type].get(path):
                        new_dict[element_type][path] = {} 

                    if not new_dict[element_type][path].get(base_name):
                        new_dict[element_type][path][base_name] = []

                    new_dict[element_type][path][base_name].append(filename)

                    if (len(new_dict[element_type][path].get(base_name)) > 1):
                        filtered_dict[element_type][path][base_name] = new_dict[element_type][path].get(base_name)

        return(filtered_dict)

    def build_catalog(self, file_structure_type):
        NON_SITE_ELEMENTS = ['metadata', 'data']

        self.read(file_structure_type)
        self.set_attributes_by_file_structure_type(file_structure_type)
        metadata_directory = os.path.join(self.site_directory, self.site.get_element_directory('metadata'))

        for element_type, sub_directory in self.site_structure.items():
            element_type = element_type.lower()

            # Don't process metadata like any other project element
            if element_type in NON_SITE_ELEMENTS:
                continue

            element_directory = Element.get_element_path(self.site, file_structure_type, element_type)

            # If Element Directory Does Not Exist that's OK
            if not os.path.exists(element_directory):
                continue

            file_dict = Common.get_files_recursively(element_directory)

            for full_path, d in file_dict.items():
                if element_type == 'page':
                    element = Page(self.site, full_path=full_path)
                else:
                    element = Element(self.site, element_type, full_path=full_path)

                key = element.get('key')
                metadata_filename = element.get_metadata_path()
                filename = element.get_filename()

                item = self.get_catalog_item(file_structure_type, element_type, key)

                catalog_id = item['id']
                catalog_checksum = item['checksum']
                current_checksum = Common.calculate_checksum(full_path)

                modified = catalog_checksum != current_checksum

                item = {
                    'id': catalog_id,
                    'key': key,
                    'filename': filename,
                    'path': full_path,
                    'element_type': element_type,
                    'metadata_filename': metadata_filename,
                    'checksum': current_checksum,
                    'modified': modified
                }

                if Common.file_exists(full_path):
                    self.set_catalog_item(file_structure_type, element_type, key, item)
                else:
                    self.remove_catalog_item(file_structure_type, element_type, key)

        matching_files = self.get_duplicate_elements(file_structure_type)

        if matching_files:
            print("Error: You may not have two elements with the same name but different extensions in the same directory.")

            for element_type, paths in matching_files.items():
                print(f"Element Type: {element_type}")

                for directory, item_dict in paths.items():
                    print(f"  Directory: {directory}")
                    print("\n".join([f"    - {file}" for file in item_dict.values()]))

                print("")

            exit(1)

        self.write

