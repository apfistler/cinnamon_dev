# lib/widget/widget_template_loader.py

import os
from jinja2 import Environment, FileSystemLoader

class WidgetTemplateLoader:
    @staticmethod
    def load_template(widget_dir, template_name):
        template_filename = f"{template_name}/{template_name}.html"
        template_path = os.path.join(widget_dir, template_filename)

        # Check if the file exists
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template file not found: {template_path}")

        env = Environment(loader=FileSystemLoader(widget_dir))
        return env.get_template(template_filename)
