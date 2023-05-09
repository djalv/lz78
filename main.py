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
	out_file = "out/" + name_file + ".z78"
else:
	out_file = sys.argv[3]
t = patricia.Trie()

with codecs.open(in_file, 'r', encoding="utf-8") as f:
	f_out = codecs.open(out_file, 'w')
	content = f.readlines()
	words = []
	
	for i in content:
		words.append(i.split())

	cnt = 0
	for i in words:
		if i == []:
			k = '\\n'
			t.insert(k, cnt)
			cnt += 1
		for k in i:
			t.insert(k, cnt)
			cnt += 1

	'''
	for i in range(cnt):
		print(i)
		word = t.search_key(i).string
		if word == '\\n':
			f_out.write("\n")
		else:
			f_out.write(word)
		f_out.write(" ")
		#print(t.search_key(i).string, end=" ")
	'''
	#print(t.search('\\n')[-1])
	#print(t.search_key(7))
	#t.print()
	lz78.encode(t, f_out)