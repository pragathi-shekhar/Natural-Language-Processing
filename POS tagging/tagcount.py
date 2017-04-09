import json
import copy
import re
import sys

from collections import Counter

try:
	fName = sys.argv[1]
except:
	print "Usage: tagcount.py <input file name>"
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
N = 0
# nTags = 0

for word in words:
	list = word.split ('/')
	
	try:
		if list[1] not in thisDict:
			thisDict[list[1]] = {"count": 0}
			
		thisDict[list[1]]["count"] += 1
		N += 1
	except:
		print list
	
	
for POS in thisDict:
	thisDict[POS]["probability"] = float (thisDict[POS]["count"]) / N



print "Total Number of Unique Tags: ", len (thisDict)

	
with open ("tagCount.json", "w") as file:
	json.dump (thisDict, file, indent = 4, sort_keys = True)
	file.close ()

