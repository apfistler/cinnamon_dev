# page.py

import os
import sys

from lib.base_content import BaseContent
from lib.page.page_template import PageTemplate
from lib.page.page_parser import PageParser

class Page(BaseContent):
    def __init__(self, site, page_metadata):
        from .page_template import PageTemplate  # Import inside the class to avoid circular import

        self.type = 'page'
        self.site = site
        self.page_metadata = page_metadata
        self.id = page_metadata.get('id')
        self.path = self._generate_path()
        self.page_template_filename = self.page_metadata.template

        super().__init__(content_id=self.id, content_path=self.path, metadata={})
        self.content = self.open_and_parse()

        self.page_template = PageTemplate(self.site, self.page_metadata, self.page_template_filename, self.content)

        # Apply the page_template
        self.apply_page_template()
    
    def get_content(self):
        return self.get('content')

    def _generate_path(self):
        # Replace '.' with '/' in the page ID
        id_path = self.id.replace('.', '/')

        # Construct the full path
        page_path = os.path.join(self.site.site_dir, 'pages', f"{id_path}.html")
        return page_path

    def exists(self):
        # Check if the page file exists
        return os.path.isfile(self.path)

    def open_and_parse(self):
        # Open the page file and read its content
        with open(self.path, 'r', encoding='utf-8') as file:
            page_content = file.read()

        # Convert page_metadata to dictionary
        page_metadata_dict = self.page_metadata.to_dict()

        # Parse the content
        parsed_content = PageParser.parse(page_content, self.site.site_dir, page_metadata_dict)

        return parsed_content

    def apply_page_template(self):
        page_template_content = self.page_template.get_content()
        if '&{{page}}' in page_template_content:
            # Replace &{{page}} with the page content
            self.content = page_template_content.replace('&{{page}}', self.content)

