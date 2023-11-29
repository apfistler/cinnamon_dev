from .base_content import BaseContent

class Page(BaseContent):
    REQUIRED_FIELDS = ['title']
    
    def __init__(self, page_id, page_path, metadata):
        super().__init__(page_id, page_path, metadata)
        # Add any additional page-specific functionality here

