import time
import difflib
import Levenshtein
from fuzzywuzzy import fuzz, process

start_time = time.time()
haystack = {}
needle = "zyomi"

#FuzzyWuzzy is slow, use sequencematcher to pare down results 
with open('/usr/share/dict/words', 'r') as fh:
	haystack = {line.lower() 
			for line in fh 
			if difflib.SequenceMatcher(None, needle, line).ratio() > .70}

print haystack
print process.extractOne(needle, haystack)
