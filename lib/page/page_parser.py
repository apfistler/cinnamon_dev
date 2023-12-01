# lib/page/page_parser.py

import re
from lib.base_content import BaseContent
from lib.widget.widget import Widget  # Adjust the import path accordingly

class PageParser:
    def __init__(self, site_dir, data):
        self.data = data

    @staticmethod
    def parse(content, site_dir, page_metadata_dict):
        widget_dir = f'{site_dir}/widgets'

        def replace(match):
            placeholder = match.group(1)
            try:
                value = PageParser.evaluate_nested_value(placeholder, page_metadata_dict)

                # Check if the value is a list (array)
                if isinstance(value, list):
                    # Join array elements with <br/>
                    return '<br/>'.join(map(str, value))

                return str(value)
            except (NameError, KeyError, IndexError):
                print(f"Error: Placeholder '{placeholder}' not found in page_metadata_dict.")
                return match.group(0)

        def process_widget(match):
            widget_input = match.group(1)
            widget = Widget(widget_input, widget_dir)
            return widget.generate_output()

        # Initialize content_with_widgets
        content_with_widgets = content

        # Replace other placeholders
        content_with_placeholder_sub = re.sub(r'#\{\{([^}]*)\}\}', replace, content)

        # Process widgets first
        parsed_content = re.sub(r'@\{\{([^}].*)\}\}', process_widget, content_with_placeholder_sub)

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
