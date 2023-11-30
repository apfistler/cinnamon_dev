from .base_content import BaseContent
import os
from .page_parser import PageParser  # Assuming you have a separate module for PageParser

class Page(BaseContent):

    def __init__(self, site, page_metadata):
        from .template import Template  # Import inside the class to avoid circular import

        self.type = 'page'
        self.site = site
        self.page_metadata = page_metadata
        self.id = page_metadata.get('id')
        self.path = self._generate_path()
        self.template_filename = self.page_metadata.template

        print(f"Template filename is {self.template_filename}")

        super().__init__(content_id=self.id, content_path=self.path, metadata={})
        self.content = self.open_and_parse()

        self.template = Template(self.site, self.page_metadata, self.template_filename)

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
        parsed_content = PageParser.parse(page_content, page_metadata_dict)

        return parsed_content
