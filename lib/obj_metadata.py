from .base_content import BaseContent

class Obj_Metadata(BaseContent):
    REQUIRED_FIELDS = ['name', 'type']
    
    def __init__(self, obj_metadata_id, obj_metadata_path, data):
        super().__init__(obj_metadata_id, obj_metadata_path, data)
        # Add any additional obj_metadata-specific functionality here

        # Check the 'type' field and add 'title' to required fields if type is 'page'
        if self.type == 'page':
            self.REQUIRED_FIELDS.append('title')

        self.check_required_fields()

        # Add any additional obj_metadata-specific functionality here

    def check_required_fields(self):
        super().check_required_fields()  # Call the base class method

