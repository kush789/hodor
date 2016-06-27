import sys

with open("../data/verbs.txt", 'r') as fp:

	"""
		Load a verb list

	"""

	verbs = fp.readlines()

for i in range(len(verbs)):

	"""
		Clean the verb list
	
	"""

	verbs[i] = verbs[i].strip("\r\n")
	verbs[i] = verbs[i].lower()

def getSyllables(name):

	"""
		Takes a name, returns the syllables

	"""

	import pyphen
	pyphen.language_fallback('nl_NL_variant1')
	
	'nl_NL' in pyphen.LANGUAGES
	dic = pyphen.Pyphen(lang='nl_NL')
	syllables = dic.inserted(name).split("-")

	return syllables

def generateRegexPermutations(pattern):

	"""
		Generates regex permuations recursively

	"""

	if len(pattern) == 1:
		return [pattern]
	else:
		set_ = generateRegexPermutations(pattern[:-1])
		newSet = []

		currentLetter = pattern[-1]

		for perm in set_:
			newSet.append(perm + currentLetter)
			newSet.append(perm + currentLetter + "([A-z])*")

		return list(set(newSet))

def getAllVerbMatches(pattern):

	"""
		Get all verbs including letters in pattern,
		the sequence remains in order.

		For ex abc -> [a*b*c*, a*b*c, a*bc*, a*bc, abc*]
	"""

	verbSet = []

	allRegexPerms = generateRegexPermutations(pattern)

	for regex in allRegexPerms:
		verbSet += getVerbMatches(pattern, regex)

	return verbSet
	
def getVerbMatches(pattern, regexPattern):

	"""
		Tries to find verbs matching regex
	"""

	import re
	import itertools

	verbSet = []

	for verb in verbs:
		rematch = re.match(regexPattern, verb)

		if rematch is not None:
			verbSet.append(rematch.group(0))

	return verbSet

if __name__ == "__main__":
	name = sys.argv[1]
	name = name.lower()

	syllables = getSyllables(name)

	for syllable in syllables:

		print getAllVerbMatches(syllable)
