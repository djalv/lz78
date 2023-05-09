import sys
import codecs
import patricia
import lz78

argc = len(sys.argv)
opt = sys.argv[1]
in_file = sys.argv[2]

if argc < 4:
	name_file = in_file.split('.')[0]
	name_file = name_file.split('/')[1]
	out_file = "out/" + name_file
	if opt == '-c':
		out_file += ".z78"
	elif opt == '-d':
		out_file += ".txt"
else:
	out_file = sys.argv[3]

with codecs.open(in_file, 'r', encoding="utf-8") as f:
	f_out = codecs.open(out_file, 'w')
	content = f.readlines()
	words = []
	
	for i in content:
		words.append(i.split())

	if opt == '-c':
		t = patricia.Trie()
		cnt = 0

		for i in words:
			if i == []:
				k = '\\n'
				t.insert(k, cnt)
				cnt += 1
			for k in i:
				t.insert(k, cnt)
				cnt += 1
		lz78.encode(t, f_out)
	
	elif opt == '-d':
		lz78.decode(words, f, f_out)
