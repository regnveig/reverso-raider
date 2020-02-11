from urllib.parse import quote
from urllib.request import Request, urlopen
import datetime
import json
import os
import random

GLOBAL_CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
GLOBAL_LANG = ["arabic", "german", "english", "spanish", "french", "hebrew", "italian", "japanese", "dutch", "polish", "portuguese", "romanian", "russian", "turkish"] # arabic and hebrew not work :(
GLOBAL_MAX_PHRASE_LENGTH = 96

def new_mimicry():
	
	with open(GLOBAL_CURRENT_DIR + "/user_agents.txt", 'rt') as agents_file: agents = agents_file.readlines()
	mim_dict = dict()
	mim_dict["User-Agent"] = random.choice(agents)[:-1]
	exp_date = datetime.datetime.now() + datetime.timedelta(days=7)
	mim_dict["Expire Date"] = exp_date.strftime("%Y-%m-%d")
	with open(GLOBAL_CURRENT_DIR + "/mimicry.json", 'wt') as mimfile: json.dump(mim_dict, mimfile)

def reverso_get(source_language, target_language, phrase):
	
	if not os.path.exists(GLOBAL_CURRENT_DIR + "/mimicry.json"): new_mimicry()
	with open(GLOBAL_CURRENT_DIR + "/mimicry.json", 'rt') as mimfile: mimicry = json.load(mimfile)
	if datetime.datetime.strptime(mimicry["Expire Date"], "%Y-%m-%d") < datetime.datetime.now(): new_mimicry()
	del mimicry["Expire Date"]
	
	phrase = quote(phrase.replace(' ', '+'))
	url = "https://context.reverso.net/translation/" + source_language + "-" + target_language + "/" + phrase
	request = Request(url, headers=mimicry)
	content = urlopen(request).read().decode("utf8")
	
	return content
