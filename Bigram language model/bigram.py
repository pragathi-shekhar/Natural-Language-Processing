import re
import json
import sys
import os
import copy
from itertools import tee, islice, izip
from collections import Counter

def tagCheck (wOne, wTwo):
	if wTwo != "-" and wTwo != "/":
		try:
			wTwo = '</' + (re.findall (r"\w+", wTwo))[0] + '>'
		except:
			print wOne + " " + wTwo
			return True
	if wOne == wTwo:
		return True
	else:
		return False

try:
	fName = sys.argv [1]
except:
	print "Usage: bigram.py <fname>.txt"
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
	
tuples = Counter (izip (words, islice (words, 1, None)))
thisDict = {}

with open ("unigram.json", "r") as file:
	uniJson = json.load (file)
	file.close ()

for (wOne, wTwo) in tuples:
	if tagCheck (wOne, wTwo) == False:
		tupDict = {}
		tupDict["count"] = tuples[(wOne, wTwo)]
		tupDict["probability"] = float (tupDict["count"]) / uniJson[wOne]["count"]
		thisDict[wOne + " " + wTwo] = copy.deepcopy (tupDict)
	
with open ("bigram.json", "w") as file:
	json.dump (thisDict, file, indent = 3)
	file.close ()

print "File Written.."