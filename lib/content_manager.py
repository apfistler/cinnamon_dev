import os
from .yaml_parser import YamlParser
from .site import Site
from .obj_metadata import Obj_Metadata

class ContentManager:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.sites = self.load_sites()

    def load_sites(self):
        site_dir = self.base_dir
        sites = []
        for site_id in os.listdir(site_dir):
            site_path = os.path.join(site_dir, site_id)
            site_metadata_path = os.path.join(site_path, 'site.yaml')
            site_metadata = YamlParser.parse_yaml(site_metadata_path)
            site = Site(site_id, site_path, site_metadata)
            site.obj_metadata_items = self.load_obj_metadata_items(site)
            sites.append(site)
        return sites

    def load_obj_metadata_items(self, site):
        obj_metadata_dir = os.path.join(site.path, 'metadata')
        obj_metadata_items = []
        for root, dirs, files in os.walk(obj_metadata_dir):
            for file in files:
                if file.endswith('.yaml'):
                    obj_metadata_id = os.path.relpath(os.path.join(root, file), obj_metadata_dir)
                    obj_metadata_id = obj_metadata_id.replace(os.path.sep, '.')[:-5]  # Remove '.yaml' extension
                    obj_metadata_path = os.path.join(root, file)
                    data = YamlParser.parse_yaml(obj_metadata_path)
                    obj_metadata = Obj_Metadata(obj_metadata_id, obj_metadata_path, data)
                    obj_metadata_items.append(obj_metadata)
        return obj_metadata_items

    def get_all_sites(self):
        return self.sites

    def get_all_obj_metadata_items(self):
        all_obj_metadata_items = [obj_metadata for site in self.sites for obj_metadata in site.obj_metadata_items]
        return all_obj_metadata_items

