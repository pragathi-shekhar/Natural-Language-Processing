import sys
import string
import json
import re
import copy
import os
import math
from collections import Counter

if len (sys.argv) < 2:
	print "Usage: training.py <dir where neg and pos are subdirectories containing files>"
	quit (1)

def vocab (mTrainingFiles):
	vocabulary = {"words": {}, "wordcount": {}}
	for dir in mTrainingFiles:
		if dir not in vocabulary["wordcount"]:
			vocabulary["wordcount"][dir] = 0
		os.chdir (dir)
		for file in mTrainingFiles[dir]:
			words = re.findall ("\w+", open (file).read())
			try:
				words = filter (lambda a: a != "", words)
			except:
				"Do Nothing!"
					
			for word in words:
				if word not in vocabulary["words"]:
					vocabulary["words"][word] = {}
					for d in subDir:
						vocabulary["words"][word][d] = {}
						vocabulary["words"][word][d]["count"] = 0
						
				vocabulary["words"][word][dir]["count"] += 1
				vocabulary["wordcount"][dir] += 1
		os.chdir ("..")
	return copy.deepcopy (vocabulary)
	
module = 0
moduleFileIndex = 0

lenUniqueWordsInModules = []

subDir = ["pos", "neg"]
curDir = sys.argv[1]
os.chdir (curDir)
modules = {}
moduleTestingFiles = {}
moduleTrainingFiles = {}

while moduleFileIndex < 1000:
	moduleTrainingFiles[module] = {}
	moduleTestingFiles[module] = {}
	
	for dir in subDir:
		moduleTrainingFiles[module][dir] = []
		moduleTestingFiles[module][dir] = []
	
	# print "Processing Module: ", (module + 1), "..."
	for dir in subDir:
		os.chdir (dir)
		tFiles = []
		files = os.listdir (".")
		files.sort ()
		for i in xrange (moduleFileIndex, moduleFileIndex + 100):
			tFiles.append (files[i])
		tFiles = set (tFiles)
		files = set (files)
		moduleTrainingFiles[module][dir].extend (files.difference (tFiles))
		moduleTestingFiles[module][dir].extend (tFiles)
		os.chdir ("..")
	
	# Files Processing
	temp = {}
	temp = vocab (moduleTrainingFiles[module])
	lenUniqueWordsInModules.append (len (temp["words"]))
	modules[module] = copy.deepcopy (temp)
	
	# print "Module ", (module + 1), " processing completed\n"
	moduleFileIndex += 100
	module += 1
	
for module in modules:
	for word in modules[module]["words"]:
		for dir in modules[module]["words"][word]:
			modules[module]["words"][word][dir]["mle"] = math.log (float (modules[module]["words"][word][dir]["count"] + 1) / (lenUniqueWordsInModules[module] + modules[module]["wordcount"][dir]), 2)

accuracy = {}
os.chdir (curDir)
for module in modules:
	accuracy[module] = {}
	count = 0
	os.chdir ("pos")
	for file in moduleTestingFiles[module]["pos"]:
		scorepos = float (len (moduleTrainingFiles[module]["pos"])) / (len (moduleTrainingFiles[module]["pos"]) + len (moduleTrainingFiles[module]["neg"]))
		scoreneg = float (len (moduleTrainingFiles[module]["neg"])) / (len (moduleTrainingFiles[module]["pos"]) + len (moduleTrainingFiles[module]["neg"]))
		
		words = re.findall ("\w+", open (file).read())
		try:
			words = filter (lambda a: a != "", words)
		except:
			"Do Nothing!"
			
		for word in words:
			try:
				scorepos += modules[module]["words"][word]["pos"]["mle"]
			except:
				scorepos += float (1) / (lenUniqueWordsInModules[module] + modules[module]["wordcount"]["pos"])
			try:
				scoreneg += modules[module]["words"][word]["neg"]["mle"]
			except:
				scoreneg += float (1) / (lenUniqueWordsInModules[module] + modules[module]["wordcount"]["neg"])
		
		if scorepos > scoreneg:
			count += 1

	os.chdir ("..")
	os.chdir ("neg")
	for file in moduleTestingFiles[module]["neg"]:
		scorepos = float (len (moduleTrainingFiles[module]["pos"])) / (len (moduleTrainingFiles[module]["pos"]) + len (moduleTrainingFiles[module]["neg"]))
		scoreneg = float (len (moduleTrainingFiles[module]["neg"])) / (len (moduleTrainingFiles[module]["pos"]) + len (moduleTrainingFiles[module]["neg"]))
		
		words = re.findall ("\w+", open (file).read())
		try:
			words = filter (lambda a: a != "", words)
		except:
			"Do Nothing!"
			
		for word in words:
			try:
				scorepos += modules[module]["words"][word]["pos"]["mle"]
			except:
				scorepos += float (1) / (lenUniqueWordsInModules[module] + modules[module]["wordcount"]["pos"])
			try:
				scoreneg += modules[module]["words"][word]["neg"]["mle"]
			except:
				scoreneg += float (1) / (lenUniqueWordsInModules[module] + modules[module]["wordcount"]["neg"])
		
		if scorepos < scoreneg:
			count += 1

	os.chdir ("..")
	accuracy[module]["count"] = count
	accuracy[module]["accuracy"] = float (count) / (len (moduleTestingFiles[module]["neg"]) + len (moduleTestingFiles[module]["pos"]))

avg = 0.0
for module in accuracy:
	avg += accuracy[module]["accuracy"]
	print "Module ", (module + 1), ":" 
	print "Count: ", accuracy[module]["count"]
	print "Accuracy: ", accuracy[module]["accuracy"], "\n"

print "Average Accuracy: ", (avg / len (accuracy)) * 100 , "%"
