#!/usr/bin/python3

from lib.config import Config
from lib.site.site import Site

def main():
    config = Config()
    config.initialize()

    site = Site(config, 'system', 'afistler')

if __name__ == '__main__':
    main()

