# page_template.py

import os
import shlex
import re
from .page_parser import PageParser  # Import inside the class to avoid circular import
from .base_content import BaseContent

class PageTemplate(BaseContent):
    def __init__(self, site, page_metadata, page_template_filename, page_content):
        self.site = site
        self.page_metadata = page_metadata
        self.path = self._generate_path(page_template_filename)
        self.type = 'page_template'
        self.page_content = shlex.quote(page_content.replace('\n', '\\n'))
        self.content = self.open_and_parse()

    def get_content(self):
        return self.get('content')

    def _generate_path(self, filename):
        # Check if the page_template filename is a partial path
        if not filename.startswith('/'):
            # If it's a partial path, assume it's relative to the site's directory
            page_template_path = os.path.join(self.site.site_dir, filename)
        else:
            # If it's already a full path, use it as is
            page_template_path = filename

        return page_template_path

    def open_and_parse(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            page_template_content = file.read()

        page_template_metadata_dict = self.page_metadata.to_dict()
        parsed_content = PageParser.parse(page_template_content, self.site.site_dir, page_template_metadata_dict)

        return parsed_content

