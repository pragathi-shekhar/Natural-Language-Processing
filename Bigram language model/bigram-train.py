import subprocess
import json
import sys
import os

if len (sys.argv) < 5:
	print "Usage: bigram-train.py -text training_file -lm lm_file"
	quit ()

try:
	fName = sys.argv [((sys.argv).index ("-text") + 1)]
	oFile = sys.argv [((sys.argv).index ("-lm") + 1)]
except:
	print "Usage: bigram-train -text training_file -lm lm_file"
	quit ()

process = subprocess.Popen(['python', 'unigram.py', fName], stdout = sys.stdout, stderr = sys.stderr)
out, err = process.communicate()

if err is not None:
	print "Problem encountered while executing unigram.py"
	quit ()

process = subprocess.Popen(['python', 'bigram.py', fName], stdout = sys.stdout, stderr = sys.stderr)
out, err = process.communicate()

if err is not None:
	print "Problem encountered while executing bigram.py"
	quit ()

process = subprocess.Popen(['python', 'backoff_weight.py'], stdout = sys.stdout, stderr = sys.stderr)
out, err = process.communicate()

if err is not None:
	print "Problem encountered while executing backoff_weight.py"
	quit ()
	
process = subprocess.Popen(['python', 'perplexity.py'], stdout = sys.stdout, stderr = sys.stderr)
out, err = process.communicate()

if err is not None:
	print "Problem encountered while executing perplexity.py"
	quit ()
	
with open ("unigram.json", "r") as file:
	uniJson = json.load (file)
	file.close ()

with open ("bigram.json", "r") as file:
	biJson = json.load (file)
	file.close ()
	
with open ("alpha.json", "r") as file:
	alJson = json.load (file)
	file.close ()

try:
	# file = open (fName, "w")
	file = open (oFile, "w")
except:
	print "Failed creating files"
	quit()
	
line = "unigrams:\n"
file.write (line)

for word in uniJson:
	line = str (uniJson[word]["probability"]) + "\t" + word + "\t" + str (alJson[word]) + "\n"
	file.write (line)
	
line = "bigrams:\n"
file.write (line)

for tuple in biJson:
	word = '\t'.join (tuple.split (' '))
	line = str (biJson[tuple]["probability"]) + "\t" + word + "\n"
	file.write (line)

file.close ()
print "Process completed.."

os.remove ("unigram.json")
os.remove ("bigram.json")
os.remove ("alpha.json")