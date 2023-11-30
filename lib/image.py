from .base_content import BaseContent
import os
from .yaml_parser import YamlParser

class Image(BaseContent):
    REQUIRED_FIELDS = ['name', 'category']

    def __init__(self, site, image_path):
        self.site = site
        self.path = image_path
        self.name = os.path.basename(image_path)
        self.category = self._get_category(image_path)

        self.metadata = {}  # Initialize metadata attribute
        self.metadata['name'] = self.name
        self.metadata['path'] = self.path
        self.metadata['category'] = self.category


        # Load metadata if available
        self.load_metadata()

        super().__init__(content_id=self.name, content_path=image_path, metadata=self.metadata)

    def _get_category(self, image_path):
        # Extract the category from the image path
        relative_path = os.path.relpath(image_path, self.site.site_dir)
        category_path = os.path.dirname(relative_path)
        # Remove the 'img' prefix if present
        if category_path.startswith('img' + os.path.sep):
            category_path = category_path[len('img' + os.path.sep):]
        category = category_path.replace(os.path.sep, '.')

        return category





    def load_metadata(self):
        # Look for metadata file in the site's metadata/img directory
        metadata_dir = os.path.join(self.site.site_dir, 'metadata', 'img')
        metadata_file_path = os.path.join(metadata_dir, f"{self.name}.yaml")

        # Parse metadata if the file exists
        if os.path.isfile(metadata_file_path):
            metadata_data = YamlParser.parse_yaml(metadata_file_path)
            self.metadata.update(metadata_data)
