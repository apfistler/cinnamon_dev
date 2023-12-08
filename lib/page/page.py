# page.py

import os
import sys
from pprint import pprint

from lib.page.page_parser import PageParser
from lib.page.page_template import PageTemplate
from lib.element.element import Element
from bs4 import BeautifulSoup

class Page(Element):
    def __init__(self, site, full_path=None, key=None):
        self.site = site
        self.element_type = 'page'
        super().__init__(site, self.element_type, full_path=full_path, key=key)

        self.template_filename = os.path.join(self.site.get_site_directory(), self.metadata.collective_params.get('template'))
        content = self.parse_page()
        content = self.apply_page_template(content)

        self.content = self.format_content(content)
        print(self.content)


    def format_content(self, content):
        # Default value if 'indent' is not present in collective_params
        page_indent = self.metadata.collective_params.get('indent', 2)

        # Rest of your code
        soup = BeautifulSoup(content, 'html.parser')
        formatted_html = self._prettify_with_indentation(soup, indent=page_indent)
        return str(formatted_html)

    def _prettify_with_indentation(self, soup, indent):
        pretty_html = soup.prettify()
        lines = pretty_html.split("\n")
        indented_html = ""
        for line in lines:
            indented_html += " " * indent + line + "\n"

        return indented_html

    def open(self):
        # Open the page file and read its content
        with open(self.path, 'r', encoding='utf-8') as file:
            content = file.read()

        return(content)

    def parse(self, page_content):
        metadata_dict = self.metadata.collective_params.to_dict()

        # Parse the content
        parsed_content = PageParser.parse(page_content, self.site.get_site_directory(), metadata_dict)

        return parsed_content

    def parse_page(self):
        content = self.open();
        content = self.parse(content)

        return content


    def apply_page_template(self, content):
        self.template = PageTemplate(self.site, self, full_path=self.template_filename)
        template_content = self.template.get_content()

        if '&{{page}}' in template_content:
            content = template_content.replace('&{{page}}', content)

        return content

        
