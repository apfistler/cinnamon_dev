# lib/page/page_template.py

import os
import re

from lib.page.header.header_manager import HeaderManager
from lib.page.page_parser import PageParser
from lib.base_content import BaseContent

class PageTemplate(BaseContent):
    def __init__(self, site, page_metadata, page_template_filename):
        self.site = site
        self.page_metadata = page_metadata
        self.path = self._generate_path(page_template_filename)
        self.type = 'page_template'
        self.content = self.open_and_parse()

    def get_content(self):
        return self.get('content')

    def _generate_path(self, filename):
        if not filename.startswith('/'):
            page_template_path = os.path.join(self.site.site_dir, filename)
        else:
            page_template_path = filename
        return page_template_path

    def open_and_parse(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            page_template_content = file.read()

        page_template_metadata_dict = self.page_metadata.to_dict()

        # Get custom headers based on the header case specified in the metadata
        #header_case = page_template_metadata_dict.get('header_case', 'default')

        # Insert custom headers after the <head> tag
        page_template_content = self.insert_custom_headers(page_template_content)

        parsed_content = PageParser.parse(page_template_content, self.site.site_dir, page_template_metadata_dict)
        return parsed_content

    def insert_custom_headers(self, content):
        head_tag_index = content.find('<head>')

        header = HeaderManager(self.site, self.page_metadata)
        custom_headers = header.get_custom_headers()

        if head_tag_index != -1:
            return content[:head_tag_index + len('<head>')] + '\n' + custom_headers + content[head_tag_index + len('<head>'):]
        else:
            return content

