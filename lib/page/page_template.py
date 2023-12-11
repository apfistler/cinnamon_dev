# lib/page/page_template.py

import os
import re

from lib.page.header.header_manager import HeaderManager
from lib.page.page_parser import PageParser
from lib.element.element import Element

class PageTemplate(Element):
    def __init__(self, site, page, full_path=None, key=None):
        self.page = page
        self.site_directory = site.get_site_directory()
        self.metadata = page.get('metadata')
        self.metadata_dict = self.metadata.all.to_dict()
        self.element_type = 'template'

        super().__init__(site, self.element_type, full_path=full_path, key=key)
        self.content = self.parse_template()

    def open(self):
        # Open the page file and read its content
        with open(self.path, 'r', encoding='utf-8') as file:
            content = file.read()

        return(content)

    def get_content(self):
        return self.content

    def parse_template(self):
        content = self.open()

        page_parser = PageParser(self.page)
        content = page_parser.parse(content)
        template_content = self.insert_custom_headers(content)
        content = page_parser.parse(template_content)
        

        return content

    def insert_custom_headers(self, content):
        head_tag_index = content.find('<head>')

        header = HeaderManager(self.site, self.metadata_dict)
        custom_headers = header.get_custom_headers()

        if head_tag_index != -1:
            return content[:head_tag_index + len('<head>')] + '\n' + custom_headers + content[head_tag_index + len('<head>'):]
        else:
            return content

