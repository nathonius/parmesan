#!/usr/bin/env python3
import argparse
from ParmAnalyzer import ParmAnalyzer
from ParmParser import ParmParser

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', help='Make output verbose', action='store_true', default=False)
args = parser.parse_args()

parm_analyzer = ParmAnalyzer(args.verbose)
parm_analyzer.update_manifest()
parm_parser = ParmParser(args.verbose)
parm_parser.parse_manifest()