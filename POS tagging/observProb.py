import json
import re
import copy
from itertools import tee, islice, izip
from collections import Counter
import sys

try:
	fName = sys.argv[1]
except:
	print "Usage: observProb.py <input file name>"
	quit (1)

sentences = re.findall (".*", open (fName).read())

try:
	sentences = filter (lambda a: a != "", sentences)
	sentences = filter (lambda a: a != "\t", sentences)
except:
	"Do Nothing!"

words = []
for sentence in sentences:
	sentence = "<s>/<s> " + sentence + " <es>/<es>"
	words.extend (sentence.split (' '))

thisDict = {}
for word in words:
	list = word.split ('/')
	key = list[0] + " " + list[1]
	try:
		if key not in thisDict:
			thisDict[key] = {"count": 0}
			
		thisDict[key]["count"] += 1
	except:
		print list

try:
	with open ("tagCount.json", "r") as file:
		tCount = json.load (file)
		file.close ()
except:
	print "tagCount.json not accessible\nDying...\n"
	quit (1)
	
for key in thisDict:
	tag = key.split (' ')[1]
	try:
		cTag = tCount[tag]["count"]
	except:
		cTag = 1
		# "If the Tag is not found, what to do?"
		
	thisDict[key]["probability"] = float (thisDict[key]["count"]) / cTag
	
with open ("obProb.json", "w") as file:
	json.dump (thisDict, file, indent = 3, sort_keys = True)
	file.close ()