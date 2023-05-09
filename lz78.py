import sys
import codecs
import patricia


def encode(trie, f_out):
	trie.fix_idx()
	trie.encode(f_out)

def decode(f_in, f_out):
	pass
