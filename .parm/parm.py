#!/usr/bin/env python3
import argparse
import json
import os.path as path
from Logger import Logger


def main():
    arg_parser = argparse.ArgumentParser()
    # All arguments can be set in parm-settings.cfg, but these take priority
    arg_parser.add_argument('-v', '--verbose', help='Make output verbose', action='store_true', default=False)
    args = arg_parser.parse_args()

    # Read options and args into parameters
    parameters = get_parameters(args)
    # Create logger
    logger = Logger(parameters)
    # Read Manifest


def get_parameters(cli_args):
    """cli_args is a Namespace object, so just a blank class. Running vars(args) returns a
    dictionary of attributes and values. The goal of this function is to read in options
    from the config file and command line, with cli args taking priority."""
    cli_args = vars(cli_args)
    # Get path to config file
    parm_path = path.dirname(__file__)
    cfg_path = path.join(parm_path, "parm-settings.cfg")
    if not path.isfile(cfg_path):
        raise FileNotFoundError("parm-settings.cfg not found")

    # Open the config file
    with open(cfg_path, 'r') as fp:
        try:
            parameters = json.load(fp)
        except ValueError:
            raise ValueError("Could not decode parm-settings.cfg. Check json format.")
    # Overwrite any params present in both the config file and cli args
    for value in cli_args.keys():
        parameters[value] = cli_args[value]
    # Add the base path of the .parm folder to the parameters, useful in many places
    parameters["parm_path"] = parm_path
    return parameters


if __name__ == "__main__":
    main()
