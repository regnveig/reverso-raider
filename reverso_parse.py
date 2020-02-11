from html.parser import HTMLParser
import pandas
import re

# FIXME Arabic and hebrew cannot be parsed :(

class ReversoParser(HTMLParser):
	
	__index = ["source", "target"]
	__build = pandas.DataFrame(columns=__index)
	__row = None
	__current = None
	__started = False
	
	def is_example(self, lst):
		for element in lst:
			if element[0] != 'class': continue
			else:
				if 'example' in element[1]: return True
		return False
	
	def handle_starttag(self, tag, attrs):
		if (tag == 'div') and self.is_example(attrs): self.__row = pandas.Series(['', ''], index=self.__index)
		if (tag == 'div') and ('class', 'src ltr') in attrs: self.__current = "source"
		if (tag == 'div') and ('class', 'trg ltr') in attrs: self.__current = "target"
		if (tag == 'span') and (self.__current is not None) and ('class', 'text') in attrs: self.__started = True
		if (tag == 'em') and (self.__current is not None): self.__row[self.__current] += "*"
	
	def handle_endtag(self, tag):
		if (tag == 'span') and self.__started:
			if self.__current == "target": self.__build = self.__build.append(self.__row, ignore_index=True)
			self.__started = False
			self.__current = None
		if (tag == 'em') and (self.__current is not None): self.__row[self.__current] += "*"
		if tag == 'html': self.__build = self.__build.applymap(lambda x: re.sub(" +", " ", x).lstrip().rstrip())
	
	def handle_data(self, data):
		if self.__current is not None: self.__row[self.__current] += str(data)
	
	def examples(self): return self.__build

def reverso_parse(content):
	
	content = content.replace('\n', ' ')
	parser = ReversoParser()
	parser.feed(content)
	
	return parser.examples()
