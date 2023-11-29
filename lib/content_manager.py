import os
from .yaml_parser import YamlParser
from .site import Site
from .metadata import Metadata

class ContentManager:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.sites = self.load_sites()

    def load_sites(self):
        site_dir = self.base_dir
        sites = []
        for site_id in os.listdir(site_dir):
            site_path = os.path.join(site_dir, site_id)
            site_config_path = os.path.join(site_path, 'site.yaml')
            site_config = YamlParser.parse_yaml(site_config_path)
            site = Site(site_id, site_path, site_config)
            site.metadata_items = self.load_metadata_items(site)
            sites.append(site)
        return sites

    def load_metadata_items(self, site):
        metadata_dir = os.path.join(site.path, 'metadata')
        metadata_items = []
        for root, dirs, files in os.walk(metadata_dir):
            for file in files:
                if file.endswith('.yaml'):
                    metadata_id = os.path.relpath(os.path.join(root, file), metadata_dir)
                    metadata_id = metadata_id.replace(os.path.sep, '.')[:-5]  # Remove '.yaml' extension
                    metadata_path = os.path.join(root, file)
                    data = YamlParser.parse_yaml(metadata_path)
                    metadata = Metadata(metadata_id, metadata_path, data)
                    metadata_items.append(metadata)
        return metadata_items

    def get_all_sites(self):
        return self.sites

    def get_all_metadata_items(self):
        all_metadata_items = [metadata for site in self.sites for metadata in site.metadata_items]
        return all_metadata_items

