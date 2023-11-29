from .base_content import BaseContent

class Obj_Metadata(BaseContent):
    REQUIRED_FIELDS = ['name', 'type']
    
    def __init__(self, obj_metadata_id, obj_metadata_path, data):
        super().__init__(obj_metadata_id, obj_metadata_path, data)
        # Add any additional obj_metadata-specific functionality here

