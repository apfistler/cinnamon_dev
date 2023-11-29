import os
from .yaml_parser import YamlParser
from .metadata import Metadata

class MetadataManager:
    def __init__(self, site_dir):
        self.site_dir = site_dir
        self.metadata_items = self.load_metadata_items()

    def load_metadata_items(self):
        metadata_items = []
        data_dir = os.path.join(self.site_dir, 'data', 'metadata_items')

        for root, dirs, files in os.walk(data_dir):
            for file in files:
                if file.endswith(".yaml"):
                    metadata_id = self.get_metadata_id(root, file)
                    metadata_path = os.path.join(root, file)
                    data = YamlParser.parse_yaml(metadata_path)
                    metadata = Metadata(metadata_id, metadata_path, data)
                    metadata_items.append(metadata)

        return metadata_items

    def get_metadata_id(self, root, file):
        relative_path = os.path.relpath(os.path.join(root, file), os.path.join(self.site_dir, 'data'))
        metadata_id = relative_path.replace(os.path.sep, '.')  # Replace '/' with '.'
        return f"{metadata_id[:-5]}.#{data['name']}" if 'name' in data else metadata_id

