# lib/page/header/header_manager.py

class HeaderManager:
    def __init__(self, site, page_metadata):
        self.site = site
        self.page_metadata = page_metadata

    def get_custom_headers(self):
        # Add your logic to retrieve custom headers based on site and page_metadata
        # You can use self.site and self.page_metadata to access the necessary information
        custom_headers = "!!!!HELLO WORLD THIS IS MY CUSTOM HEADER!!."  # Replace with your actual logic

        return custom_headers
