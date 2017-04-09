import os
import sys
import json
import math
import re
from collections import Counter
from itertools import tee, islice, izip

if len (sys.argv) < 5:
	print "Usage: bigram-test -text training_file -lm lm_file"
	quit ()

try:
	fName = sys.argv [((sys.argv).index ("-text") + 1)]
	iFile = sys.argv [((sys.argv).index ("-lm") + 1)]
except:
	print "Usage: bigram-train.py -text training_file -lm lm_file"
	quit ()

try:
	file = open (iFile, "r")
except:
	print "Unable to open input file..\nDying.."
	quit()

uniJson = {}
biJson = {}
alJson = {}
lines = file.readlines ()

for line in lines[1:]:
	list = line.split('\t')
	list = filter (lambda a: a != "", list)
	
	if list[0] == "bigrams:\n":
		break
	try:
		uniJson[list[1]] = {}
	except:
		print list
		quit()
	uniJson[list[1]]["probability"] = float (list[0])
	alJson[list[1]] = float ((list[2].split ('\n'))[0])

for line in lines[(lines.index ("bigrams:\n") + 1):]:
	list = line.split('\t')
	list = filter (lambda a: a != "", list)
	try:
		biJson[str (list[1]) + " " + str ((list[2].split ('\n'))[0])] = {"probability": float (list[0])}
	except:
		print list
		quit ()
	
list = re.findall ("<\w+>.*</\w+>", open (fName).read())
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

uniDict = {}
for (word, count) in unigram.most_common():
	uniDict[word] = count

print "Number of words in test file:", wCount
tuples = Counter (izip (words, islice (words, 1, None)))

def katzProbability (wOne, wTwo, wCount, uniDict, alJson):
	return (math.log ((alJson[wOne] * uniDict[wTwo]["probability"]), 2))

logList = []
for (wOne, wTwo) in tuples:
	if wOne + " " + wTwo in biJson:
		logList.append (math.log (biJson[wOne + " " + wTwo]["probability"], 2))
	else:
		logList.append (katzProbability (wOne, wTwo, wCount, uniJson, alJson))

exponent = -1 * (float (1) / wCount) * (sum (logList)) + 1
print "Exponent: ", exponent
print "Perplexity is: ", (2 ** exponent)	
