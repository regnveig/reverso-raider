__version__ = "0.02"
__author__ = "regnveig"

from reverso_get import *
from reverso_parse import *
from termcolor import colored

import argparse
import os
import sys

def highlighter(string): return ''.join([(colored(part[1], 'yellow') if (part[0] % 2) == 1 else part[1]) for part in enumerate(string.split('*'))])

def cli_output(data):
	if data.empty: print(f"\nNo results by this query!", end='\n')
	else:
		print(str(), end='\n')
		for row in data.iterrows(): print(f"{str(row[0] + 1)}:\t{highlighter(row[1]['source'])}\n\t{highlighter(row[1]['target'])}", end='\n', file=sys.stdout)

def createParser():
	Default_parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="Reverso Raider: free tool to get Reverso Context examples", epilog="Author: regnveig")
	Default_parser.add_argument('-v', '--version', action='version', version=__version__)
	Default_parser.add_argument ('-s', '--source', required=True, type=str, choices=GLOBAL_LANG, dest="source", help='Source language')
	Default_parser.add_argument ('-t', '--target', required=True, type=str, choices=GLOBAL_LANG, dest="target", help='Target language')
	Default_parser.add_argument ('-p', '--phrase', default=None, dest="phrase", help='Phrase to translate')
	return Default_parser

if __name__ == '__main__':
	parser = createParser()
	namespace = parser.parse_args(sys.argv[1:])
	if namespace.phrase is not None: cli_output(reverso_parse(reverso_get(namespace.source, namespace.target, str(namespace.phrase))))
	else:
		Tag = f"\nMode: {namespace.source.capitalize()} ==> {namespace.target.capitalize()} (enter phrase, or press Ctrl+D to exit)"
		print(f"\n*** Reverso Raider ***", end='\n')
		print(Tag, end='\n')
		for query in sys.stdin:
			cli_output(reverso_parse(reverso_get(namespace.source, namespace.target, str(query))))
			print(Tag, end='\n')
