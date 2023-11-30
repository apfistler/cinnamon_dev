import re
from pprint import pprint

class PageParser:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def parse(content, page_metadata_dict):

        def replace(match):
            placeholder = match.group(1)
            try:
                value = PageParser.evaluate_nested_value(placeholder, page_metadata_dict)
                return str(value)
            except (NameError, KeyError, IndexError):
                print(f"Error: Placeholder '{placeholder}' not found in page_metadata_dict.")
                return match.group(0)

        parsed_content = re.sub(r'#\{\{([^}]*)\}\}', replace, content)
        return parsed_content

    @staticmethod
    def evaluate_nested_value(placeholder, data):
        # Split the placeholder into nested levels
        levels = placeholder.split('.')
        value = data

        # Traverse the nested levels to get the final value
        for level in levels:
            # Handle array indexing
            if '[' in level and ']' in level:
                array_name, index_str = level.split('[')
                index = int(index_str.rstrip(']'))
                value = value[array_name][index]
            else:
                value = value[level]

        return value

