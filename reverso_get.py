GLOBAL_LANG = ["arabic", "german", "english", "spanish", "french", "hebrew", "italian", "japanese", "dutch", "polish", "portuguese", "romanian", "russian", "turkish"]
GLOBAL_MAX_PHRASE_LENGTH = 96

def new_mimicry(current_dir):
	
	with open(current_dir + "/user_agents.txt", 'rt') as agents_file: agents = agents_file.readlines()
	mim_dict = dict()
	mim_dict["User-Agent"] = random.choice(agents)[:-1]
	exp_date = datetime.datetime.now() + datetime.timedelta(days=7)
	mim_dict["Expire Date"] = exp_date.strftime("%Y-%m-%d")
	print(mim_dict)
	with open(current_dir + "/mimicry.json", 'wt') as mimfile: json.dump(mim_dict, mimfile)

def reverso_get(source_language, target_language, phrase):
	
	from urllib.parse import quote
	from urllib.request import Request, urlopen
	import datetime
	import json
	import os
	import random
	
	current_dir = os.path.abspath(os.path.dirname(__file__))
	
	# check data
	assert source_language in GLOBAL_LANG, f"Unknown source language ({source_language})"
	assert target_language in GLOBAL_LANG, f"Unknown target language ({target_language})"
	assert source_language != target_language, f"Source and target languages must be different"
	assert type(phrase) is str, f"Phrase must be string type"
	assert (len(phrase) > 0) and (len(phrase) <= GLOBAL_MAX_PHRASE_LENGTH), f"Phrase must contain 1..{GLOBAL_MAX_PHRASE_LENGTH} symbols"
	
	# prepare mimicry data
	if not os.path.exists(current_dir + "/mimicry.json"): new_mimicry(current_dir)
	with open(current_dir + "/mimicry.json", 'rt') as mimfile: mimicry = json.load(mimfile)
	if datetime.datetime.strptime(mimicry["Expire Date"], "%Y-%m-%d") < datetime.datetime.now(): new_mimicry(current_dir)
	del mimicry["Expire Date"]
	
	# get html
	phrase = quote(phrase.replace(' ', '+'))
	url = "https://context.reverso.net/translation/" + source_language + "-" + target_language + "/" + phrase
	request = Request(url, headers=mimicry)
	content = urlopen(request).read().decode("utf8")
	
	return content
