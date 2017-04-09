import json
import re
import copy
from itertools import tee, islice, izip
from collections import Counter
import sys

try:
	fName = sys.argv[1]
except:
	print "Usage: transProb.py <input file name>"
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

POS = []
for word in words:
	POS.append ((word.split('/'))[1])
	
tuples = Counter (izip (POS, islice (POS, 1, None)))
thisDict = {}

with open ("tagCount.json", "r") as file:
	tagCnt = json.load (file)
	file.close ()

for (tOne, tTwo) in tuples:
	tupDict = {}
	tupDict["count"] = tuples[(tOne, tTwo)]
	tupDict["probability"] = float (tupDict["count"]) / tagCnt[tOne]["count"]
	thisDict[tOne + " " + tTwo] = copy.deepcopy (tupDict)

if "<es> <s>" in thisDict:
	del thisDict["<es> <s>"]
	
with open ("transProb.json", "w") as file:
	json.dump (thisDict, file, indent = 3)
	file.close ()
