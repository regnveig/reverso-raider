__version__ = "0.02"
__author__ = "regnveig"

from reverso_get import *
from reverso_parse import *
from termcolor import colored
import argparse
import os
import sys

def error_message(e): print(f"Error: {format(e)}", end='\n', file=sys.stderr)

def highlighter(string): return ''.join([(colored(part[1], 'yellow') if (part[0] % 2) == 1 else part[1]) for part in enumerate(string.split('*'))])

def cli_output(data):
	
	if data.empty:
		print(f"No results by this query!", end='\n', file=sys.stdout)
	else:
		for row in data.iterrows(): print(f"{str(row[0] + 1)}:\t{highlighter(row[1]['source'])}\n\t{highlighter(row[1]['target'])}", end='\n', file=sys.stdout)

def createParser():
	
	Default_parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="Reverso Raider: free tool to get Reverso Context examples", epilog="Author: regnveig")
	Default_parser.add_argument('-v', '--version', action='version', version=__version__)
	Default_parser.add_argument ('-s', '--source', required=True, type=str, choices=GLOBAL_LANG, dest="source", help='Source language')
	Default_parser.add_argument ('-t', '--target', required=True, type=str, choices=GLOBAL_LANG, dest="target", help='Target language')
	Default_parser.add_argument ('-p', '--phrase', default="", type=str, dest="phrase", help='Phrase to translate')
	
	return Default_parser

if __name__ == '__main__':
	
	parser = createParser()
	namespace = parser.parse_args(sys.argv[1:])
	
	try:
		assert namespace.source != namespace.target, f"Source and target languages must be different"
		assert len(namespace.phrase) <= GLOBAL_MAX_PHRASE_LENGTH, f"Phrase must contain 1..{GLOBAL_MAX_PHRASE_LENGTH} symbols"
	except AssertionError as e:
		error_message(e)
		exit(1)
	
	if namespace.phrase != "":
		try:
			cli_output(reverso_parse(reverso_get(namespace.source, namespace.target, namespace.phrase)))
		except Exception as e:
			error_message(e)
			exit(1)
	else:
		Tag = f"Mode: {namespace.source.capitalize()} --> {namespace.target.capitalize()} (enter phrase, or press Ctrl+D to exit)"
		print(Tag, end='\n', file=sys.stdout)
		
		for query in sys.stdin:
			# TODO Check query
			try:
				cli_output(reverso_parse(reverso_get(namespace.source, namespace.target, str(query))))
			except Exception as e:
				error_message(e)
			print(Tag, end='\n', file=sys.stdout)
		
		print(f"Bye!", end='\n', file=sys.stdout)
