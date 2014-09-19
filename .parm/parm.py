#!/usr/bin/env python3
import argparse
from ParmManifestGenerator import ParmManifestGenerator as generator
from ParmManifestParser import ParmManifestParser as parser

argparser = argparse.ArgumentParser()
argparser.add_argument('-v', '--verbose', help='Make output verbose', action='store_true', default=False)
args = argparser.parse_args()

parm_generator = generator(args.verbose)
parm_generator.update_manifest()
parm_parser = parser(args.verbose)
parm_parser.parse_manifest()