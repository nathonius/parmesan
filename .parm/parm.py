#!/usr/bin/env python3
import argparse
from ParmManifestGenerator import ParmManifestGenerator as generator
from ParmManifestParser import ParmManifestParser as parser
from ParmContentGenerator import ParmContentGenerator as content_generator
from ParmWriter import ParmWriter as writer
from ParmLogger import ParmLogger
from ParmOptions import ParmOptions

argparser = argparse.ArgumentParser()
argparser.add_argument('-v', '--verbose', help='Make output verbose', action='store_true', default=False)
args = argparser.parse_args()

logger = ParmLogger(args.verbose)
options = ParmOptions(args.verbose)
parm_generator = generator(logger, options)
parm_generator.update_manifest()
parm_parser = parser(logger, options)
paths = parm_parser.parse_manifest()
print(paths)
content_generator = content_generator(logger, options)
content = content_generator.generate(paths)
parm_writer = writer(logger, options)
parm_writer.write(content)