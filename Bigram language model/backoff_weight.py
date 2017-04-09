import os
import sys
import json

def goodTuring (N2, N1, CountOfWordOne, numMulFactor):
	return ((2 * float (N2) * numMulFactor) / (N1 * CountOfWordOne)) 
	
def discountFactor (listPMLGivenWordOne):
	return sum (listPMLGivenWordOne)

def maxLikelihoodEstimation (listPML):
	return sum (listPML)
	
def alpha (wordOne, N1, N2, uniJson, biJson):
	wordTwoList = []
	tupleProbCountGreaterThanOne = []
	tupleProbCountEqualToOne = []

	for word in uniJson:
		if wordOne + " " + word in biJson:
			wordTwoList.append (word)
			count = biJson[wordOne + " " + word]["count"]
			prob = biJson[wordOne + " " + word]["probability"]
			if count == 1:
				tupleProbCountEqualToOne.append (prob) # Good Turing Computation
			elif count > 1:
				tupleProbCountGreaterThanOne.append (prob) # Discount Factor Computation
	
	# Discount Factor Computation
	DFVal = discountFactor (tupleProbCountGreaterThanOne)
	
	# Good Turing Computation
	GTVal = goodTuring (N2, N1, uniJson[wordOne]["count"], len (tupleProbCountEqualToOne))
	
	wordTwoListProb = []
	for word in wordTwoList:
		wordTwoListProb.append (uniJson[word]["probability"])
		
	# Maximum Likelihood Estimation
	mLE = maxLikelihoodEstimation (wordTwoListProb)
	
	if (1 - DFVal - GTVal) == 0.0:
		return ((1 - 0.99) / (1 - mLE))
	else:
		return ((1 - DFVal - GTVal) / (1 - mLE))
	
with open ("unigram.json", "r") as file:
	uniJson = json.load (file)
	file.close()

with open ("bigram.json", "r") as file:
	biJson = json.load (file)
	file.close()

N1 = 0
N2 = 0

for tuple in biJson:
	# print tuple
	if biJson[tuple]["count"] == 2:
		N2 += 1
	elif biJson[tuple]["count"] == 1:
		N1 += 1
		
print "N1 is ", N1
print "N2 is ", N2

thisDict = {}
for word in uniJson:
	thisDict[word] = alpha (word, N1, N2, uniJson, biJson)
	# print "alpha (" + word + ") : " + str (thisDict[word])

with open ("alpha.json", "w") as file:
	json.dump (thisDict, file, indent = 3, sort_keys = True)
	file.close()