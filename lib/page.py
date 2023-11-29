import os
from .yaml_parser import YamlParser

class Page:
    def __init__(self, page_id, page_path, metadata):
        self.id = page_id
        self.path = page_path
        self.metadata = metadata

