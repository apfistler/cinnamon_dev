# lib/page/header/header_manager.py
from pprint import pprint
import yaml

class HeaderManager:
    def __init__(self, site, page_metadata):
        self.site = site
        self.page_metadata = page_metadata

    def get_custom_headers(self):
        # Add your logic to retrieve custom headers based on site and page_metadata
        # You can use self.site and self.page_metadata to access the necessary information
        headers = self.get_simple_elements(['css', 'fonts', 'js'])
        headers += self.get_from_metadata_header()


        print(headers)
        exit(1)
        
         

        return headers

    def get_simple_elements(self, types):
        result_str = ''

        for type in types:
            # Check if the element is an attribute of self.page_metadata and is not None
            if hasattr(self.page_metadata, element) and getattr(self.page_metadata, element) is not None:
                data = getattr(self.page_metadata, element)

                for value in data:
                    dict = {}

                    if type in ['css', 'font']:
                       ary = [ 
                            'rel': 'stylesheet'
                            'type': 'text/css',
                            'href': value
                            } ]

                       dict = append_to_dict(d, 'link'
                    else if type == 'js'
                      

                            
                result_str += f'@{{{{tag type="{element}" data="{data}"}}}}\n'

        return result_str

    def get_from_metadata_header(self):
        cmd_str = ''

        if hasattr(self.page_metadata, 'head') and self.page_metadata.head:
            header_str = ''

            yaml_str = yaml.dump(self.page_metadata.head)
            dict = yaml.safe_load(yaml_str)
 
            for tag, values in dict.items():
                cmd_str += f'@{{{{tag type="{tag}" values="{values}"}}}}'

        return cmd_str

    def append_to_dict(dictionary, key, value):
        if key not in dictionary:
            dictionary[key] = []

        dictionary[key].append(value)

        return(dictionary)


