# template.py

import os
import shlex
import re
from .page_parser import PageParser  # Import inside the class to avoid circular import
from .base_content import BaseContent

class Template(BaseContent):
    def __init__(self, site, page_metadata, template_filename, page_content):
        self.site = site
        self.page_metadata = page_metadata
        self.path = self._generate_path(template_filename)
        self.type = 'template'
        self.page_content = shlex.quote(page_content.replace('\n', '\\n'))
        self.content = self.open_and_parse()

    def get_content(self):
        return self.get('content')

    def _generate_path(self, filename):
        # Check if the template filename is a partial path
        if not filename.startswith('/'):
            # If it's a partial path, assume it's relative to the site's directory
            template_path = os.path.join(self.site.site_dir, filename)
        else:
            # If it's already a full path, use it as is
            template_path = filename

        return template_path

    def open_and_parse(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            template_content = file.read()

        template_metadata_dict = self.page_metadata.to_dict()
        parsed_content = PageParser.parse(template_content, self.site.site_dir, template_metadata_dict)

        return parsed_content

