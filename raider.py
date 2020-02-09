#!/bin/python3

__version__ = "0.01"
__author__ = "regnveig"

from reverso_get import *
from reverso_parse import *

import argparse
import os
import sys

def createParser():
	Default_parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="Reverso Raider: free tool to get Reverso Context examples", epilog="Author: regnveig")
	Default_parser.add_argument('-v', '--version', action='version', version=__version__)
	Default_parser.add_argument ('-s', '--source', required=True, type=str, choices=GLOBAL_LANG, dest="source", help='Source language')
	Default_parser.add_argument ('-t', '--target', required=True, type=str, choices=GLOBAL_LANG, dest="target", help='Target language')
	Default_parser.add_argument ('-p', '--phrase', required=True, type=str, dest="phrase", help='Phrase to translate')
	return Default_parser

if __name__ == '__main__':
	parser = createParser()
	namespace = parser.parse_args(sys.argv[1:])
	data = reverso_parse(reverso_get(namespace.source, namespace.target, namespace.phrase))
	
	for row in data.iterrows(): print(f"{str(row[0] + 1)}: {row[1]['source']}\n{row[1]['target']}\n", end='\n', file=sys.stdout)
