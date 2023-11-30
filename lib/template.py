from .base_content import BaseContent
import os
from .page_parser import PageParser  # Assuming you have a separate module for PageParser

class Template(BaseContent):
    def __init__(self, site, page_metadata, template_filename):
        super().__init__(content_id='', content_path='', metadata={})
        self.site = site
        self.page_metadata = page_metadata
        self.path = self._generate_path(template_filename)
        self.type = 'template'
        self.content = self.open_and_parse()

        print(self.content)
        exit

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
        parsed_content = PageParser.parse(template_content, template_metadata_dict)

        return parsed_content

