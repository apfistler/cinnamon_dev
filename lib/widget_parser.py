# widgets/widget_parser.py

import re
import yaml

class WidgetParser:
    @staticmethod
    def parse_template_name(widget_input):
        match = re.search(r'@\{{\s*([\w\s]+)\s*', widget_input)
        if match:
            return match.group(1).strip()

    @staticmethod
    def parse_input_data(widget_input):
        match = re.search(r'input\s*=\s*["\']({.*})["\']', widget_input)
        if match:
            input_data_str = match.group(1)
            return yaml.safe_load(input_data_str)

