#!/usr/bin/python3

from lib.config import Config
from lib.content_manager import ContentManager

def main():
    config = Config()
    config.initialize()

    base_dir = config.get('site_dir')

    content_manager = ContentManager(base_dir)
    all_sites = content_manager.get_all_sites()

    # Print all sites and their properties
    print("All Sites:")
    for site in all_sites:
        print(f"\nSite ID: {site.id}")
#        site.display_all()

        # Display all page_metadata_items for the site
        print("\nAll Metadatas:")
        for page_metadata in site.page_metadata_items:
            print(f"\nMetadata ID: {page_metadata.id}")
            page_metadata.display_all()

    # Extract all site IDs
    all_site_ids = [site.id for site in all_sites]

    # Print all site IDs
    print("\nAll Site IDs:")
    for site_id in all_site_ids:
        print(site_id)

if __name__ == '__main__':
    main()

