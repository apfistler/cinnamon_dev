# page.py

import os
import sys
from bs4 import BeautifulSoup
from pprint import pprint

from lib.element.element import Element
from lib.page.page_parser import PageParser
from lib.page.page_template import PageTemplate

class Page(Element):
    def __init__(self, site, full_path=None, key=None):
        self.element_type = 'page'
        super().__init__(site, self.element_type, full_path=full_path, key=key)

        self.template_filename = os.path.join(self.site.get('site_directory')[self.file_location_type], self.metadata.collective_params.get('template'))
        self.content = self.parse_page()
        self.apply_page_template()
#        self.apply_template(content)

#        print(self.content)

###        self.page_template = PageTemplate(self.site, self.page_metadata, self.page_template_filename)

        # Apply the page_template
        #self.apply_page_template()
    
    def get_content(self):
        page_indent = 2

        if self.page_metadata.has_attr('indent'):
            page_indent = self.page_metadata.indent

        soup = BeautifulSoup(self.content, 'html.parser')
        formatted_html = self._prettify_with_indentation(soup, indent=page_indent)
        return str(formatted_html)

    def _prettify_with_indentation(self, soup, indent):
        pretty_html = soup.prettify()
        lines = pretty_html.split("\n")
        indented_html = ""
        for line in lines:
            indented_html += " " * indent + line + "\n"
        return indented_html

    def _generate_path(self):
        # Replace '.' with '/' in the page ID
        id_path = self.id.replace('.', '/')

        # Construct the full path
        page_path = os.path.join(self.site.site_dir, 'pages', f"{id_path}.html")
        return page_path

    def open(self):
        # Open the page file and read its content
        with open(self.path, 'r', encoding='utf-8') as file:
            page_content = file.read()

        return(page_content)

    def parse(self, page_content):
        metadata_dict = self.metadata.collective_params.to_dict()

        # Parse the content
        parsed_content = PageParser.parse(page_content, self.site.get('site_directory'), metadata_dict)

        return parsed_content

    def parse_page(self):
        content = self.open();
        content = self.parse(content)

        return content

    def apply_page_template(self):
        template = PageTemplate(self.site, self, full_path=self.template_filename)
        #page_template_content = self.page_template.get_content()

        #if '&{{page}}' in page_template_content:
            # Replace &{{page}} with the page content
        #    self.content = page_template_content.replace('&{{page}}', self.content)
