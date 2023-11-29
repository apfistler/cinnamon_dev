import os
from .yaml_parser import YamlParser
from .site import Site
from .page import Page

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
            site.pages = self.load_pages(site)
            sites.append(site)
        return sites

    def load_pages(self, site):
        page_dir = os.path.join(site.path, 'pages')
        pages = []
        for root, dirs, files in os.walk(page_dir):
            for file in files:
                if file.endswith('.yaml'):
                    page_id = os.path.relpath(os.path.join(root, file), page_dir)
                    page_id = page_id.replace(os.path.sep, '.')[:-5]  # Remove '.yaml' extension
                    page_path = os.path.join(root, file)
                    page_metadata = YamlParser.parse_yaml(page_path)
                    page = Page(page_id, page_path, page_metadata)
                    pages.append(page)
        return pages

    def get_all_sites(self):
        return self.sites

    def get_all_pages(self):
        all_pages = [page for site in self.sites for page in site.pages]
        return all_pages

