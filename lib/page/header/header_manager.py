# lib/page/header/header_manager.py

class HeaderManager:
    def __init__(self, site, page_metadata):
        self.site = site
        self.page_metadata = page_metadata

    def get_custom_headers(self):
        # Add your logic to retrieve custom headers based on site and page_metadata
        # You can use self.site and self.page_metadata to access the necessary information
        custom_headers = "!!!!HELLO WORLD THIS IS MY CUSTOM HEADER!!."  # Replace with your actual logic
        header = self.get_elements(['css', 'fonts', 'js'])

        print(header)
        exit(1)
        
         

        return custom_headers

    def get_elements(self, elements):
        result_str = ''

        for element in elements:
            # Check if the element is an attribute of self.page_metadata and is not None
            if hasattr(self.page_metadata, element) and getattr(self.page_metadata, element) is not None:
                data = getattr(self.page_metadata, element)
                result_str += f'@{{{{{element} data="{data}"}}}}\n'

        return result_str
