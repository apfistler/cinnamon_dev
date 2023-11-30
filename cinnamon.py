#!/usr/bin/python3

from lib.config import Config
from lib.content_manager import ContentManager
from lib.page import Page

def main():
    config = Config()
    config.initialize()

    base_dir = config.get('site_dir')

    content_manager = ContentManager(base_dir)
    all_sites = content_manager.get_all_sites()

    # Iterate through all sites
    for site in all_sites:
#        print(f"\nSite ID: {site.id}")

        # Iterate through all page_metadata_items for the site
#        print("\nAll Metadatas:")
        for page_metadata in site.page_metadata_items:
            name = page_metadata.get('name')
            page_id = page_metadata.get('id')
#            print(f"Page Name is #{name}")
#            print(f"Page ID is #{page_id}")

            # Create a Page object
            page = Page(site, page_metadata)

            # Check if the page exists
            if page.exists():
                # Open and parse the page
                parsed_content = page.open_and_parse()
                print(f"The page '{page_id}' exists. Parsed Content:")
                print(parsed_content)
            else:
                print(f"The page '{page_id}' does not exist.")

        # Display all images for the site
#        print("\nAll Images:")
#        all_images = content_manager.get_all_images(site)
#        for image in all_images:
#            print(f"\nImage ID: {image.id}")

if __name__ == '__main__':
    main()

