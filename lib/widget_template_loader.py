# widgets/widget_template_loader.py

from jinja2 import Environment, FileSystemLoader

class WidgetTemplateLoader:
    @staticmethod
    def load_template(widget_dir, template_name):
        print(f'Widget dir is {widget_dir}')
        template_filename = f"{template_name}/{template_name}.html"
        env = Environment(loader=FileSystemLoader(widget_dir))
        return env.get_template(template_filename)

