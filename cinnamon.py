#!/usr/bin/python3

import os
import argparse
from lib.config import Config

def main():
    config = Config()
    config.initialize()

    # Example of using get and set
    property_to_get = 'admin'
    value = config.get(property_to_get)
    print(f"Value of '{property_to_get}': {value}")

    property_to_set = 'new_property'
    new_value = 'New Value'
    config.set(property_to_set, new_value)
    print(f"Value of '{property_to_set}' after setting: {config.get(property_to_set)}")

    config.display_all()

if __name__ == '__main__':
    main()
