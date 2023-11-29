import os
import yaml

class Site:
    def __init__(self, site_id, name, config):
        self.site_id = site_id
        self.name = name
        self.config = config

    def __str__(self):
        return f"Site {self.site_id}: {self.name}"

    @classmethod
    def from_yaml(cls, site_id, yaml_path):
        with open(yaml_path, 'r') as file:
            config = yaml.safe_load(file)
        name = config.get('name', 'Unknown')
        return cls(site_id, name, config)


