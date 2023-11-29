#!/usr/bin/python3

import os
from lib.config import Config
from lib.site_manager import SiteManager

def main():
    config = Config()
    config.initialize()

    sites_dir = config.get('sites_dir')

    site_manager = SiteManager(sites_dir)
    all_sites = site_manager.get_all_sites()

    # Print all sites and their properties
    print("All Sites:")
    for site in all_sites:
        print(f"\nSite ID: {site.site_id}")
        site.display_all()

    # Extract all site IDs
    all_site_ids = [site.site_id for site in all_sites]

    # Print all site IDs
    print("\nAll Site IDs:")
    for site_id in all_site_ids:
        print(site_id)

if __name__ == '__main__':
    main()

