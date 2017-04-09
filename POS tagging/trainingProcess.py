import subprocess
import json
import sys
import os
import copy
import re

try:
	trainingFile = sys.argv [((sys.argv).index ("-train")) + 1]
	modelFile = sys.argv [((sys.argv).index ("-model")) + 1]
except:
	print "Usage: trainingProcess.py -train train_file -model model_file"
	quit (1)
	
process = subprocess.Popen(['python', 'tagcount.py', trainingFile], stdout = sys.stdout, stderr = sys.stderr)
out, err = process.communicate()

if err is not None:
	print "Problem encountered while executing tagCount.py"
	quit ()

process = subprocess.Popen(['python', 'transProb.py', trainingFile], stdout = sys.stdout, stderr = sys.stderr)
out, err = process.communicate()

if err is not None:
	print "Problem encountered while executing transProb.py"
	quit ()

process = subprocess.Popen(['python', 'observProb.py', trainingFile], stdout = sys.stdout, stderr = sys.stderr)
out, err = process.communicate()

if err is not None:
	print "Problem encountered while executing observProb.py"
	quit ()
	
thisDict = {}

tSentences = re.findall (".*", open (trainingFile).read())
try:
	tSentences = filter (lambda a: a != "", tSentences)
	tSentences = filter (lambda a: a != "\t", tSentences)
except:
	"Do Nothing!"

# print tSentences
tWords = {}
for s in tSentences:
	# print s
	ps = s.split (' ')
	# print ps
	for pair in ps:
		word = pair.split ('/')[0]
		if word not in tWords:
			tWords[word] = 0
tWords['<s>'] = 0
tWords['<es>'] = 0

with open ("tagCount.json", "r") as file:
	tagCount = json.load (file)
	file.close ()
	
with open ("obProb.json", "r") as file:
	obProb = json.load (file)
	file.close ()
	
with open ("transProb.json", "r") as file:
	transProb = json.load (file)
	file.close ()
	
thisDict["tagCount"] = copy.deepcopy (tagCount)
thisDict["obProb"] = copy.deepcopy (obProb)
thisDict["transProb"] = copy.deepcopy (transProb)
thisDict["tWords"] = copy.deepcopy (tWords)

with open (modelFile, "w") as file:
	json.dump (thisDict, file, indent = 4)
	file.close ()

print "File Writing Completed.."
	
os.remove ("tagCount.json")
os.remove ("obProb.json")
os.remove ("transProb.json")
