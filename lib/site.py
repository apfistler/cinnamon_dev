from .base_content import BaseContent

class Site(BaseContent):
    REQUIRED_FIELDS = ['name', 'url']
    
    def __init__(self, site_id, site_path, data):
        super().__init__(site_id, site_path, data)
        # Add any additional site-specific functionality here

