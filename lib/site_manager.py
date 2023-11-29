import os
from .site import Site
from .yaml_parser import YamlParser

class SiteManager:
    def __init__(self, sites_dir):
        self.sites_dir = sites_dir
        self.sites = self.load_sites()

    def load_sites(self):
        all_sites = []
        for filename in os.listdir(self.sites_dir):
            if filename.endswith(".yaml"):
                site_id, _ = os.path.splitext(filename)
                yaml_path = os.path.join(self.sites_dir, filename)
                site_config = YamlParser.parse_yaml(yaml_path)
                site = Site(site_id, site_config)
                all_sites.append(site)
        return all_sites

    def get_all_sites(self):
        return self.sites

