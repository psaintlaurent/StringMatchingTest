import time, sys, difflib, re
import Levenshtein
from ngram import NGram
from fuzzywuzzy import fuzz, process

#FuzzyWuzzy is slow, use sequencematcher to pare down results 
def sq_pare(needle='default', fn='/usr/share/dict/words', pth=.50):
	with open(fn, 'r') as fh:
		sq_haystack = {line 
				for line in fh 
				if difflib.SequenceMatcher(None, needle, line).ratio() - pth >= 0.0}
	return sq_haystack

#FuzzyWuzzy is slow, use Ngram approximation to pare down results
def ng_pare(needle='default', fn='/usr/share/dict/words', pth=.50):
	with open(fn, 'r') as fh:
        	ng_haystack = {line
                        	for line in fh
                        	if NGram.compare(needle, line, N=1) - pth >= 0.0}
	return ng_haystack

inp = sys.argv[1:]
rgx = re.compile('[\W_]+')
search_str, pare_type, pare_th, filename = rgx.sub('', inp[0]), inp[1], .50, '/usr/share/dict/words'

if len(inp) == 3:
	pare_th = float(inp[2]) #That's right I'm not validating my inputs before casting, it's a test, sue me
if len(inp) == 4:
	filename = inp[3]

pare_method = getattr(sys.modules[__name__], pare_type)
start_time = time.time()
haystack = pare_method(search_str, filename, pare_th)
print haystack

print '%s execution time is %s seconds.' % (pare_type, time.time() - start_time)
print process.extractOne(search_str, haystack)


