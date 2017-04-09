import json
import copy
import re
import sys

from collections import Counter

try:
	referenceFile = sys.argv [((sys.argv).index ("-ref")) + 1]
	oFile = sys.argv [((sys.argv).index ("-sys")) + 1]
except:
	print "Usage: evaluation.py -ref ref_file -sys your_output"
	quit (1)

sentences = re.findall (".*", open (oFile).read())
try:
	sentences = filter (lambda a: a != "", sentences)
	sentences = filter (lambda a: a != "\t", sentences)
except:
	"Do Nothing!"

words = []
for sentence in sentences:
	words.extend (sentence.split (' '))
	
try:
	words = filter (lambda a: a != "<s>/<s>", words)
	words = filter (lambda a: a != "", words)
except:
	"Do Nothing!"

taggedWords = []

uWordsCount = 0
kWordsCount = 0

uWordsGoodCount = 0
kWordsGoodCount = 0

for word in words:
	# print word
	badWord = False
	list = word.split ('/')
	
	if (list[0] == word):
		list = word.split ('^')
		uWordsCount += 1
		badWord = True
	
	try:
		if list[0] != '<es>' and list[1] != '<es>':
			taggedWords.append (word)
			if badWord == False:
				kWordsCount += 1
	except:
		print "Word: " + word
		print list
		quit (1)
		
sentences = re.findall (".*", open (referenceFile).read())
try:
	sentences = filter (lambda a: a != "", sentences)
	sentences = filter (lambda a: a != "\t", sentences)
except:
	"Do Nothing!"

words = []
for sentence in sentences:
	words.extend (sentence.split (' '))
	
print "Test Words:", len (words)
print "Tagged Words:", len (taggedWords)
print "Unknown Words:", uWordsCount
print "Known Words:", kWordsCount

goodCount = 0

for i in xrange (0, len (words)):
	if words[i] == taggedWords[i]:
		goodCount += 1
		kWordsGoodCount += 1
	elif words[i].replace ('/', '^') == taggedWords[i]:
		goodCount += 1
		uWordsGoodCount += 1

		
print "Unknown Good Words:", uWordsGoodCount
print "Known Good Words:", kWordsGoodCount
print "Good Count:" + str(goodCount)		
print "Known Good Count:" + str(kWordsGoodCount)		
print "Unknown Good Count:" + str(uWordsGoodCount)		
print "Accuracy, Overall: " + str (float (goodCount) / len (words))
print "Accuracy for Known words: " + str (float (kWordsGoodCount) / kWordsCount)
print "Accuracy for Unknown words: " + str (float (uWordsGoodCount) / uWordsCount)