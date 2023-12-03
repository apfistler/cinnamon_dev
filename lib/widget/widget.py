# lib/widget/widget.py

import re
import yaml

from lib.widget.widget_template_loader import WidgetTemplateLoader
from lib.base_content import BaseContent
from lib.yaml_parser import YamlParser

class Widget(BaseContent):
    def __init__(self, input_str, widget_dir):
        self.input_str = input_str
        self.widget_dir = widget_dir
        (self.template_name, self.args) = self.extract_args()
        self.path = f'{widget_dir}/{self.template_name}/{self.template_name}.html'
        # Do not return anything from __init__, just call the method

    def extract_args(self):
        # Use a regex pattern to capture the first word as the template name and the remaining string as arguments
        match = re.search(r'\s*(\w+)\s*(.*)', self.input_str)

        if match:
            template_name = match.group(1).strip()
            args_str = match.group(2).strip()

            # Use another regex to capture key-value pairs from the arguments string
            args_pattern = re.compile(r'(\w+)(?:=(?:"([^"]*)"|(\S+)))?')
            args = {key: value if value else None for key, value, _ in args_pattern.findall(args_str)}

            return template_name, args
        else:
            raise ValueError(f"Invalid input string: {self.input_str}")

    def generate_output(self):
        template = WidgetTemplateLoader.load_template(self.widget_dir, self.template_name)
        render_args = {key: yaml.safe_load(value) for key, value in self.args.items()}

        return self.trim_empty_lines(template.render(**render_args))

    def trim_empty_lines(self,output):
        lines = output.splitlines()
        non_empty_lines = filter(lambda line: line.strip(), lines)
        return '\n'.join(non_empty_lines)
