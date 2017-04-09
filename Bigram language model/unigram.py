import urllib2
import json
import copy
import re
import os
import sys
from collections import Counter

try:
	fName = sys.argv [1]
except:
	print "Usage: unigram.py <fname>.txt"
	quit ()

try:
	list = re.findall ("<\w+>.*</\w+>", open (fName).read())
except:
	print "Invalid Files.."
	quit ()
	
words = []
for sentence in list:
	words.extend (sentence.split (' '))

try:
	words = filter (lambda a: a != "", words)
	words = filter (lambda a: a != "\t", words)
except:
	"Do Nothing!"
	
wCount = len (words)
unigram = Counter (words)

print wCount

thisDict = {}

for (word, count) in unigram.most_common():
	thisWord = {}
	thisWord["count"] = count
	thisWord["probability"] = float(count) / wCount
	thisDict[word] = copy.deepcopy (thisWord)
	
with open ("unigram.json", "w") as file:
	json.dump (thisDict, file, indent = 4, sort_keys = True)
	file.close ()
