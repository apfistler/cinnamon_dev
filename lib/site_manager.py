import os
from .site import Site
from .yaml_parser import YamlParser

class SiteManager:
    def __init__(self, base_dir):
        if not os.path.exists(base_dir):
            print(f"Error: Base directory '{base_dir}' does not exist.")
            exit(1)

        self.base_dir = base_dir
        self.sites = self.load_sites()

    def load_sites(self):
        all_sites = []
        for subdir in os.listdir(self.base_dir):
            site_dir = os.path.join(self.base_dir, subdir)

            if os.path.isdir(site_dir):
                site_config_path = os.path.join(site_dir, 'site.yaml')
                
                if os.path.exists(site_config_path):
                    site_config = YamlParser.parse_yaml(site_config_path)
                    site = Site(subdir, site_config)
                    all_sites.append(site)
        
        return all_sites

    def get_all_sites(self):
        return self.sites

