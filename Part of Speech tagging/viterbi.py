import json
import os
import sys
import re
import copy
from itertools import tee, islice, izip
from collections import Counter

try:
	testFile = sys.argv [((sys.argv).index ("-test")) + 1]
	modelFile = sys.argv [((sys.argv).index ("-model")) + 1]
	oFile = sys.argv [((sys.argv).index ("-o")) + 1]
except:
	print "Usage: viterbi.py -test test_file -model model_file -o output"
	quit (1)

def maxValue (thisDict):
	value = -1
	index = -1
	prevIndex = -1
	for tagIndex in thisDict:
		if thisDict[tagIndex][0] > value:
			value = thisDict[tagIndex][0]
			prevIndex = thisDict[tagIndex][1]
			index = tagIndex
			
	return [index, value, prevIndex]

with open (modelFile, "r") as file:
	training = json.load (file)
	file.close ()

tr = copy.deepcopy (training["transProb"])
ob = copy.deepcopy (training["obProb"])
tagJson = copy.deepcopy (training["tagCount"])
tWords = copy.deepcopy (training["tWords"])

# with open ("transProb.json", "r") as file:
	# tr = json.load (file)
	# file.close ()

# with open ("obProb.json", "r") as file:
	# ob = json.load (file)
	# file.close ()
	
# with open ("tagCount.json", "r") as file:
	# tagJson = json.load (file)
	# file.close ()
	
tags = []
for tag in tagJson:
	tags.append (str (tag))

sentences = re.findall (".*", open (testFile).read())
try:
	sentences = filter (lambda a: a != "", sentences)
	sentences = filter (lambda a: a != "\t", sentences)
except:
	"Do Nothing!"

finalSentences = []
count = 1
for sentence in sentences:
	sentence = "<s> " + sentence + " <es>"
	words = sentence.split (' ')
	
	print "Processing Line " + str (count) + ": " + sentence
	count += 1
	V = {}
	for j in xrange (0, len (words)):
		V[j] = {}
		for i in xrange (0, len (tags)):
			V[j][i] = (-1.0, -1)
	
	
	for j in xrange (0, len (words)):
		for i in xrange (0, len (tags)):
			if j == 0:
				if words[j] == '<s>' and tags[i] == words[j]:
					V[j][i] = (1.0, 0)
				else:
					V[j][i] = (0.0, 0)
			else:
				for k in xrange (0, len (tags)):
					try:
						if V[j][i][0] < V[j - 1][k][0] * tr[tags[k] + " " + tags[i]]["probability"]:
							V[j][i] = (V[j - 1][k][0] * tr[tags[k] + " " + tags[i]]["probability"], k)
					except:
						if V[j][i][0] < 0:
							V[j][i] = (0.0, k)
				
				value = V[j][i][0]
				index = V[j][i][1]
				
				if words[j] in tWords:
					try:
						V[j][i] = (value * ob[words[j] + " " + tags[i]]["probability"], index)
					except:
						V[j][i] = (0.0, index)
				else:
					obUnknownWord = (float (1) / 47) * 0.1 * (float (1) / tagJson[tags[i]]["probability"])
					V[j][i] = (value * obUnknownWord, index)
	
	index = -1	
	for i in reversed (xrange (0, len (words))):
		if index < 0:
			list = maxValue (V[i])
			value = list[1]
			prevIndex = list[2]
			index = list[0]
		else:
			(value, prevIndex) = V[i][index]
			
		if words[i] in tWords:
			words[i] += "/" + tags[index]
		else:
			words[i] += "^" + tags[index]
		index = prevIndex
	
	finalSentences.append ((' '.join (words) + "\n"))
	
with open (oFile, "w") as file:
	file.write (' '.join (finalSentences))
	file.close ()