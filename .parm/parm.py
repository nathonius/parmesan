#!/usr/bin/env python3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', help='Make output verbose', action='store_true')
args = parser.parse_args()