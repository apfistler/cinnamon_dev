import os
from .yaml_parser import YamlParser
from .site import Site
from .page_metadata import Page_Metadata

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
            site.page_metadata_items = self.load_page_metadata_items(site)
            sites.append(site)
        return sites

    def load_page_metadata_items(self, site):
        page_metadata_dir = os.path.join(site.path, 'metadata')
        page_metadata_items = []
        for root, dirs, files in os.walk(page_metadata_dir):
            for file in files:
                if file.endswith('.yaml'):
                    page_metadata_id = os.path.relpath(os.path.join(root, file), page_metadata_dir)
                    page_metadata_id = page_metadata_id.replace(os.path.sep, '.')[:-5]  # Remove '.yaml' extension
                    page_metadata_path = os.path.join(root, file)
                    data = YamlParser.parse_yaml(page_metadata_path)
                    page_metadata = Page_Metadata(page_metadata_id, page_metadata_path, data)
                    page_metadata_items.append(page_metadata)
        return page_metadata_items

    def get_all_sites(self):
        return self.sites

    def get_all_page_metadata_items(self):
        all_page_metadata_items = [page_metadata for site in self.sites for page_metadata in site.page_metadata_items]
        return all_page_metadata_items


