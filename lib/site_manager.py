import os
from lib.site import Site

class SiteManager:
    def __init__(self, sites_dir):
        self.sites_dir = sites_dir
        self.sites = self.load_sites()

    def load_sites(self):
        sites = {}
        for file_name in os.listdir(self.sites_dir):
            if file_name.endswith(".yaml"):
                site_id = os.path.splitext(file_name)[0]
                yaml_path = os.path.join(self.sites_dir, file_name)
                site = Site.from_yaml(site_id, yaml_path)
                sites[site_id] = site
        return sites

    def get_site(self, site_id):
        return self.sites.get(site_id)

    def get_all_sites(self):
        return list(self.sites.values())

