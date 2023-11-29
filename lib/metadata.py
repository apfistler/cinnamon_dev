from .base_content import BaseContent

class Metadata(BaseContent):
    REQUIRED_FIELDS = ['name', 'type']
    
    def __init__(self, metadata_id, metadata_path, data):
        super().__init__(metadata_id, metadata_path, data)
        # Add any additional metadata-specific functionality here

