import os
from .yaml_parser import YamlParser
from .page import Page

class PageManager:
    def __init__(self, site_dir):
        self.site_dir = site_dir
        self.pages = self.load_pages()

    def load_pages(self):
        pages = []
        metadata_dir = os.path.join(self.site_dir, 'metadata', 'pages')

        for root, dirs, files in os.walk(metadata_dir):
            for file in files:
                if file.endswith(".yaml"):
                    page_id = self.get_page_id(root, file)
                    page_path = os.path.join(root, file)
                    metadata = YamlParser.parse_yaml(page_path)
                    page = Page(page_id, page_path, metadata)
                    pages.append(page)

        return pages

    def get_page_id(self, root, file):
        relative_path = os.path.relpath(os.path.join(root, file), os.path.join(self.site_dir, 'metadata'))
        page_id = relative_path.replace(os.path.sep, '.')  # Replace '/' with '.'
        return f"{page_id[:-5]}.#{metadata['name']}" if 'name' in metadata else page_id

