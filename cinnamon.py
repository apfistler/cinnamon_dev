#!/usr/bin/python3

import os
import sys
import argparse
import ast  # You need to import the ast module for the parse_multiple_values function

#from lib.logger import Logger
from lib.logger import Logger
from lib.config import Config
from lib.site.site import Site

VERSION = '0.1.0a1'
APPLICATION_NAME = f'Cinnamon {VERSION}'

def parse_multiple_values(value):
    try:
        # Try to parse as a list using ast.literal_eval
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        # If parsing fails, split by comma or space
        return value.replace(',', ' ').split()

def parse_args():
    parser = argparse.ArgumentParser(description=f'{APPLICATION_NAME}: Static Web Site Generator')
    parser.add_argument('--help_page', nargs='*', help='Display Help Page')
    parser.add_argument('--site', nargs='+', type=parse_multiple_values, help='Site Name(s) e.g. --site mysite')
    parser.add_argument('--cinnamon_directory', type=str, help='Cinnamon directory')
    parser.add_argument('--base_site_directory', type=str, help='Base Site directory')
    parser.add_argument('--config_directory', type=str, help='Cinnamon Configuration directory')
    parser.add_argument('--log_directory', type=str, help='Log directory')
    parser.add_argument('--file_structure_type', type=str, default='user', help='File Structure Type: user or site')
    parser.add_argument('--import', nargs='+', type=parse_multiple_values, help='Import filename(s) e.g. --import page1.html page2.html')
    parser.add_argument('--export', type=str, help="Export directory")
    return parser.parse_args()

def process_args(globals):
    args = globals['args']

    if args.help_page is not None:
        display_help_page()
        exit(1)

    if args.site is None:
        print(f'{sys.argv[0]}: --site "site1" "site2" | --site must have one or more values')
        exit(1)

    if any([args.cinnamon_directory, args.base_site_directory, args.config_directory]):
        set_custom_file_structure(globals)

def set_custom_file_structure(globals):
    args = globals['args'] 
    config = globals['config']

    file_structure_type = args.file_structure_type

    file_structure = config.get('file_structure')

    if file_structure_type not in file_structure:
        print(f"Error: File structure type '{file_structure_type}' is not defined in config.")
        exit(1)

    default_file_structure = file_structure[file_structure_type]

    base_site_directory = args.base_site_directory or default_file_structure['base_site_directory']
    config_directory = args.config_directory or default_file_structure['config_directory']
    cinnamon_directory = args.cinnamon_directory or default_file_structure['cinnamon_directory']

    # Update the file_structure dictionary
    file_structure['custom'] = {
        'cinnamon_directory': cinnamon_directory,
        'config_directory': config_directory,
        'base_site_directory': base_site_directory
    }

    # Update the 'args' dictionary with the new 'file_structure_type'
    args.file_structure_type = 'custom'

    # Update the config with the modified file_structure
    config.set('file_structure', file_structure)

def display_help_page():
    print(APPLICATION_NAME)
    print("")
    print("This is the application help page... But you are the developer of this application.  If you don't know how to use it, then we are screwed...")
    exit(0)

def main():
    globals = {
        'config' : Config(),
        'args' : parse_args()
    }

    process_args(globals)


#    site = Site(globals['config'], 'system', 'afistler')

if __name__ == '__main__':
    main()

