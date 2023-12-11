# lib/page/page_parser.py

import re
from lib.base_content import BaseContent
from lib.widget.widget import Widget  # Adjust the import path accordingly
from lib.shortcut.shortcut import Shortcut

class PageParser:
    def __init__(self, page):
        self.page = page
        self.site = page.get('site')

    def parse(self, content):
        metadata_dict = self.page.metadata.all.to_dict()

        #content = re.sub(r'(.)\{\{([^}].*)\}\}', handle_place_holders, content)

        def parse_place_holders(content):
            match_order = ['#', '%', '@']

            for symbol in match_order:
                if symbol in ['%', '@']:
                    pattern = re.escape(symbol) + r'\{\{([^}}].*)\}\}'
                elif symbol == '#':
                    pattern = re.escape(symbol) + r'\{\{([^}}]*)\}\}'

                content = re.sub(pattern, lambda match: parse_place_holder(match, symbol), content)

            return content

        def parse_place_holder(match, symbol):
            match_string = match.group(1)

            if symbol == '#':
                return process_metadata(match_string) 
            elif symbol == '%':
                return Shortcut(self.site, match_string).generate_output()
            elif symbol == '@':  # Fix: Added missing colon
                # This should be handled by the template
                if match_string == 'page':
                    return '@{{page}}'

                return  Widget(self.site, match_string).generate_output()


        def process_metadata(match_string):
            try:
                value = PageParser.evaluate_nested_value(match_string, metadata_dict)

                # Check if the value is a list (array)
                if isinstance(value, list):
                    # Join array elements with <br/>
                    return '<br/>'.join(map(str, value))

                return str(value)
            except (NameError, KeyError, IndexError):
                print(f"Error: Metadata param '{match_string}' not found in metadata_dict.")
                return match.group(0)

        content = parse_place_holders(content)
        return content

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

