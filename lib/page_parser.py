import re
from pprint import pprint


class PageParser:
    def __init__(self, data):
        self.data = data
        print("SELF DATA!!!!")
        pprint(self.data)

    def parse(content, page_metadata_dict):
        # Define a replacement function
        print("DICT!!!!!!!!!!")
        pprint(page_metadata_dict)

        def replace(match):
            placeholder = match.group(1)
            try:
                # Use eval with locals to access the dictionary
                return str(eval(placeholder, globals(), page_metadata_dict))
            except (NameError, KeyError):
                # Handle the case where the placeholder doesn't exist in the dictionary
                return match.group(0)

        # Use re.sub with the replacement function
        parsed_content = re.sub(r'#\{\{([^}]*)\}\}', replace, content)

        return parsed_content

    def _get_nested_value(self, placeholder):
        # Split the placeholder into nested levels
        levels = placeholder.split('.')
        value = self.data

        # Traverse the nested levels to get the final value
        for level in levels:
            if isinstance(value, dict):
                value = value.get(level, '')
            elif isinstance(value, list):
                try:
                    level = int(level)
                    value = value[level]
                except (ValueError, IndexError):
                    value = ''
            else:
                value = ''

        return value

# Usage example:
# parser = PageParser(data)  # Replace 'data' with your actual data
# parsed_content = parser.parse(content)  # Replace 'content' with your actual content

