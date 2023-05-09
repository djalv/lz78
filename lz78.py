import sys
import codecs
import ast
import patricia

def encode(trie, f_out):
	trie.fix_idx()
	trie.encode(f_out)

def decode(words, f_in, f_out):
	n = len(words)
	tpls = []
	strings = [""] * n
	keys = [None] * n
	idx = 0
	
	# Transforma as tuplas no texto
	# em tuplas em python
	for i in words:
		tpls.append(ast.literal_eval(i[0]))
		if len(i) > 1:
			keys[idx] = i[1:]
		idx += 1

	#Junta os prefixos da tupla
	# transformando-as em strings presentes no texto
	cnt = 0
	for i, s in tpls:
		if i == 0:
			strings[cnt] += s
		else:
			if s != '*':
				strings[cnt] += strings[i-1] + s
			else:
				strings[cnt] = strings[i-1]

		cnt += 1

	# Formata a lista strings
	cnt = 0
	strings_input = []
	for i in keys:
		if i is not None:
			for idx in i:
				strings_input.append((strings[cnt],int(idx,16)))
		cnt += 1
	strings_input.sort(key=lambda a: a[1])
	
	# Escreve no arquivo de saida
	for s, i in strings_input:
		f_out.write(s)
		if '\n' in s:
			f_out.write("\n")
		else:
			f_out.write(" ")