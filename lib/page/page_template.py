# lib/page/page_template.py

import os
import re

from lib.element.element import Element
from lib.page.header.header_manager import HeaderManager
from lib.page.page_parser import PageParser

class PageTemplate(Element):
    def __init__(self, site, page, full_path=None, key=None):
        self.page = page
        self.element_type = 'template'
        self.metadata = page.get('metadata')
        super().__init__(site, self.element_type, full_path=full_path, key=key)
        print(f"This is a template")
        self.content = self.parse_template()
        print(template)

    def get_content(self):
        return self.get('content')

    def open(self):
        # Open the page file and read its content
        with open(self.path, 'r', encoding='utf-8') as file:
            page_content = file.read()

        return(page_content)

    def parse(self, page_content):
        metadata_dict = self.metadata.collective.to_dict()

        # Parse the content
        parsed_content = PageParser.parse(page_content, self.site.get('site_directory'), metadata_dict)

        return parsed_content


    def parse_template(self):
        metadata_dict = self.page.metadata.collective_metadata.to_dict()
        content = self.open()

        page_template_content = self.insert_custom_headers(content)
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

