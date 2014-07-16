import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', help='Make output verbose', action='store_true')
parser.parse_args()