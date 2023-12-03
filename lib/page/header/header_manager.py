import yaml

class HeaderManager:
    def __init__(self, site, page_metadata):
        self.site = site
        self.page_metadata = page_metadata

    def get_custom_headers(self):
        # Add your logic to retrieve custom headers based on site and page_metadata
        # You can use self.site and self.page_metadata to access the necessary information
        headers = self.get_title()
        headers += self.get_base()
        headers += self.get_from_shortcuts(['css', 'fonts', 'js'])
        headers += self.get_from_metadata_header()
        headers += self.get_keywords()

        return headers

    def get_from_shortcuts(self, types):
        cmd_str = ''

        for element in types:
            # Check if the element is an attribute of self.page_metadata and is not None
            if hasattr(self.page_metadata, element) and getattr(self.page_metadata, element) is not None:
                data = getattr(self.page_metadata, element)

                dictionary = {}  # Initialize the 'dictionary' variable outside the loop

                for value in data:
                    values = {}  # Initialize the 'ary' variable inside the loop for each 'value'

                    if element in ['css', 'fonts']:
                        values = {
                            'rel': 'stylesheet',
                            'type': 'text/css',
                            'href': value
                        }

                    elif element == 'js':
                        values = {
                            'src': value
                        }

                    dictionary = self.append_to_dict(dictionary, 'link' if element in ['css', 'fonts'] else 'script', values)
                cmd_str += self.generate_tag_cmd(dictionary)

        return cmd_str

    def get_keywords(self):
        if hasattr(self.page_metadata, 'keywords') and self.page_metadata.keywords:
            keywords = ','.join(self.page_metadata.keywords)  # Fix the typo here (elf -> self)
            dictionary = {
                'meta': [{
                    'name': 'keywords',
                    'content': keywords
                }]
            }

        return self.generate_tag_cmd(dictionary)


    def get_from_metadata_header(self):
        cmd_str = ''

        if hasattr(self.page_metadata, 'head') and self.page_metadata.head:
            yaml_str = yaml.dump(self.page_metadata.head)
            dictionary = yaml.safe_load(yaml_str)

            cmd_str += self.generate_tag_cmd(dictionary)

        return cmd_str

    def generate_tag_cmd(self, dictionary):
        # Creates widget commands to generate header tags based on the type and values provided
        cmd_str = ''

        for tag, values in dictionary.items():
            cmd_str += f'@{{{{tag type="{tag}" values="{values}"}}}}\n'

        return cmd_str

    def get_tag(self, tag_name, attribute=None, default_value=''):
        if attribute is None:
            attribute = tag_name

        value = getattr(self.page_metadata, attribute, default_value)
        tag = f'<{tag_name}>{value}</{tag_name}>\n'
        return tag

    def get_title(self, title=None):
        return self.get_tag('title', 'title', title)

    def get_base(self, href=None):
        if href is None:
            if self.page_metadata.has_param('base'):
                href = self.page_metadata.base
            else:
                return

        tag = f'<base href="{href}" />\n'
        return tag


    def append_to_dict(self, dictionary, key, value):
        if key not in dictionary:
            dictionary[key] = []

        dictionary[key].append(value)

        return dictionary

