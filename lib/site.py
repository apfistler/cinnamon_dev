from .base_content import BaseContent

class Site(BaseContent):
    REQUIRED_FIELDS = ['name', 'url']
    
    def __init__(self, site_id, site_path, metadata):
        super().__init__(site_id, site_path, metadata)
        # Add any additional site-specific functionality here

