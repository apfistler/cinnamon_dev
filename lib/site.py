from .base_content import BaseContent

class Site(BaseContent):
    REQUIRED_FIELDS = ['name', 'url']
    
    def __init__(self, site_id, site_path, data):
        super().__init__(site_id, site_path, data)
        # Add any additional site-specific functionality here

        self.check_required_fields()

        # Add any additional obj_metadata-specific functionality here

    def check_required_fields(self):
        super().check_required_fields()  # Call the base class method

