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
        header += self.build_header()


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

    def build_header(self):
        header_str = ''

        if hasattr(self.page_metadata, 'head') and self.page_metadata.head:
            for element_data in self.page_metadata.head:
                # Check if the element_data is a dictionary
                if not isinstance(element_data, dict):
                    continue

                element_name = element_data.get('name', '')  # Adjust this based on your data structure
                if not element_name:
                    continue

                header_str += f'<{element_name} '

                attributes = element_data.get('attributes', {})
                for attribute, value in attributes.items():
                    header_str += f'{attribute}="{value}" '

                header_str = header_str.rstrip() + '>\n'

        return header_str

    def build_header(self):
        header_str = ''

        if hasattr(self.page_metadata, 'head') and self.page_metadata.head:
            for element_identifier in self.page_metadata.head:
                # Assuming you have a mapping of identifiers to dictionaries
                element_data = self.get_element_data(element_identifier)

                if not element_data:
                    continue

                element_name = element_data.get('name', '')  # Adjust this based on your data structure
                if not element_name:
                    continue

                header_str += f'<{element_name} '

                attributes = element_data.get('attributes', {})
                for attribute, value in attributes.items():
                    header_str += f'{attribute}="{value}" '

                header_str = header_str.rstrip() + '>\n'

        return header_str

    def get_element_data(self, element_identifier):
        # Define a mapping of identifiers to dictionaries
        element_mapping = {
            'meta': {'name': 'meta', 'attributes': {'http-equiv': 'Content-Type', 'content': 'text/html;'}},
            # Add more mappings as needed
        }

        return element_mapping.get(element_identifier, {})


