import argparse
import os

import yaml
from selenium.webdriver.common.keys import Keys


def parse_args():
    parser = argparse.ArgumentParser(description='Kayak Scrapper')

    parser.add_argument(
        '--config',
        type=str,
        default=None,
        help='Config file name to use. If not given, run the GUI.')

    parser.add_argument(
        '--timeout',
        type=int,
        default=5,
        help='Maximum time to wait a selenium element')
    return parser.parse_args()


def load_config(path, config_name):
    """Load YAML configuration file given its path and file name"""
    with open(os.path.join(path, config_name)) as file:
        config = yaml.safe_load(file)
    return config


def save_config(file_path, config):
    """Save configuration file to YAML"""
    with open(file_path, "w") as file:
        _ = yaml.dump(config, file)
    return config


def sort_dictionary(dic):
    """Sort dictionary by value"""
    return {k: v for k, v in sorted(dic.items(), key=lambda item: item[1])}


def clear_entire_text(element):
    """Clear text from selenium element"""
    element.send_keys(Keys.CONTROL + 'a', Keys.BACKSPACE)


def nice_print(dictionary):
    """Print more nicely a dictionary"""
    print("\n".join(f"- {k} :\t{v}" for k, v in dictionary.items()))
