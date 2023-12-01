#lib/content_manager.py

import os

from lib.yaml_parser import YamlParser
from lib.site import Site
from lib.page.page_metadata import Page_Metadata
from .image import Image

class ContentManager:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.sites = self.load_sites()
        self.images = self.load_images()

    def load_sites(self):
        site_dir = self.base_dir
        sites = []
        for site_id in os.listdir(site_dir):
            site_path = os.path.join(site_dir, site_id)
            site_metadata_path = os.path.join(site_path, 'site.yaml')
            site_metadata = YamlParser.parse_yaml(site_metadata_path)
            site = Site(site_id, site_path, site_metadata)
            
            # Updated to snake_case
            site.page_metadata_items = self.load_page_metadata_items(site)
            
            sites.append(site)
        return sites

    def load_page_metadata_items(self, site):
        page_metadata_dir = os.path.join(site.path, 'metadata/pages')
        page_metadata_items = []
        for root, dirs, files in os.walk(page_metadata_dir):
            for file in files:
                if file.endswith('.yaml'):
                    page_metadata_id = os.path.relpath(os.path.join(root, file), page_metadata_dir)
                    page_metadata_id = page_metadata_id.replace(os.path.sep, '.')[:-5]  # Remove '.yaml' extension
                    page_metadata_path = os.path.join(root, file)
                    data = YamlParser.parse_yaml(page_metadata_path)
                    page_metadata = Page_Metadata(page_metadata_id, page_metadata_path, data, site)
                    page_metadata_items.append(page_metadata)
        return page_metadata_items

    def load_images(self):
        image_dir = os.path.join(self.base_dir, 'img')
        images = []
        for root, dirs, files in os.walk(image_dir):
            for file in files:
                image_path = os.path.join(root, file)
                image = Image(self.site, image_path)
                images.append(image)
        return images

    def get_all_sites(self):
        return self.sites

    def get_all_page_metadata_items(self):
        all_page_metadata_items = [page_metadata for site in self.sites for page_metadata in site.page_metadata_items]
        return all_page_metadata_items

    def get_all_images(self, site):
        all_images = []
        for root, dirs, files in os.walk(os.path.join(site.path, 'img')):
            for file in files:
                if not file.endswith('.yaml'):
                    image_path = os.path.join(root, file)
                    image_id = os.path.relpath(image_path, site.path)
                    data_path = os.path.join(site.path, 'metadata', 'img', f"{os.path.splitext(file)[0]}.yaml")
                    data = YamlParser.parse_yaml(data_path) if os.path.isfile(data_path) else {}
                    # Pass the correct parameters to the Image constructor
                    image = Image(site, image_path)
                    all_images.append(image)
        return all_images


