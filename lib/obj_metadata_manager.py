import os
from .yaml_parser import YamlParser
from .obj_metadata import Obj_Metadata

class Obj_MetadataManager:
    def __init__(self, site_dir):
        self.site_dir = site_dir
        self.obj_metadata_items = self.load_obj_metadata_items()

    def load_obj_metadata_items(self):
        obj_metadata_items = []
        data_dir = os.path.join(self.site_dir, 'data', 'obj_metadata_items')

        for root, dirs, files in os.walk(data_dir):
            for file in files:
                if file.endswith(".yaml"):
                    obj_metadata_id = self.get_obj_metadata_id(root, file)
                    obj_metadata_path = os.path.join(root, file)
                    data = YamlParser.parse_yaml(obj_metadata_path)
                    obj_metadata = Obj_Metadata(obj_metadata_id, obj_metadata_path, data)
                    obj_metadata_items.append(obj_metadata)

        return obj_metadata_items

    def get_obj_metadata_id(self, root, file):
        relative_path = os.path.relpath(os.path.join(root, file), os.path.join(self.site_dir, 'data'))
        obj_metadata_id = relative_path.replace(os.path.sep, '.')  # Replace '/' with '.'
        return f"{obj_metadata_id[:-5]}.#{data['name']}" if 'name' in data else obj_metadata_id

