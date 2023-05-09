from longest_prefix import longest_prefix
import sys

class Node:
	def __init__(self):
		self.prefix = "#"
		self.string = "#"
		self.is_leaf = True
		self.idx = 0
		self.previous = None
		self.keys = []
		self.next = []

	def __str__(self):
		s = self.prefix + " "
		
		for keys in self.keys:
			s += str(keys) + " "
		return s

class Trie:
	def __init__(self):
		self.root = Node()
		self.size = 1

	def search(self, string):
		path = []
		self._search(self.root, string, path)
		if len(path) == 0:
			return [self.root]
		return path

	def _search(self, node, string, path):
		for nxt in node.next:
			max_prefix = longest_prefix(nxt.prefix, string)
			
			if max_prefix == 0:
				continue
			else:
				path.append(nxt)
				string_sufix = string[max_prefix:]
				self._search(nxt, string_sufix, path)
		return path

	def search_key(self, key):
		x = []
		self._search_key(self.root, key, x)
		if len(x) == 0:
			x = [self.root]
		return x[-1]

	def _search_key(self, node, key, x):
		if key in node.keys:
			x.append(node)

		for nxt in node.next:
			self._search_key(nxt, key, x)

	def insert(self, string, key):
		new_node1 = Node()
		new_node2 = Node()

		# Pesquisa o caminho que deverá ser feito para inserir
		path = self.search(string)

		# O ultimo nó será o modificado
		in_node = path[-1]

		string_sufix = string
		path_prefix = ""
		
		# Recupera os prefixo do caminho
		# e calcula o tamanho do prefixo 
		# entre a string e o prefixo do caminho
		for n in path:
			max_prefix = longest_prefix(path_prefix, string)
			if max_prefix > 0:
				string_sufix = string_sufix[max_prefix:]
			
			path_prefix += n.prefix
		
		# Se a string e o prefixo do caminho são iguais
		# é pq ja existe essa string na Trie
		if path_prefix == string:
			
			# Logo se o nó de entrada é folha armazena a chave
			if in_node.is_leaf:
				in_node.keys.append(key)
			
			# Senão procura o caractere que marca
			# o final da string e adiciona a chave	
			else:
				for leaf in in_node.next:
					if leaf.prefix == '*':
						leaf.keys.append(key)
			return

		# Adiquire a nova string que será armazenada
		max_prefix = longest_prefix(path_prefix, string)
		new_string = string[max_prefix:]

		# Se a nova string for vazia
		# Adicione o caractere que marca o final da string
		if new_string == "":
			new_string = '*'
		
		# Se o prefixo do nó de entrada tiver mais que um caractere
		# significa que podemos dividir o nó
		if len(in_node.prefix) > 1:
			# Divide o nó em dois
			# onde um será o prefixo da string
			# e o outro sufixo do nó de entrada

			max_prefix2 = longest_prefix(in_node.prefix, string_sufix)
			prefix = string_sufix[:max_prefix2]
			sufix = in_node.prefix[max_prefix2:]

			keys = in_node.keys
			previous_next = in_node.next
			previous_string = in_node.string
			previous_father = in_node.previous
			previous_idx = in_node.idx
			
			in_node.string = ""
			in_node.prefix = prefix
			in_node.is_leaf = False
			in_node.keys = []
			in_node.next = []

			if sufix == "":
				sufix = '*'
			new_node1.prefix = sufix
			new_node1.keys = keys
			new_node1.next = previous_next
						
			if len(previous_next) > 0:
				new_node1.is_leaf = False
			else:
				new_node1.is_leaf = True
				new_node1.string = previous_string
			in_node.next.append(new_node1)

			for nxt in new_node1.next:
				nxt.previous = new_node1
			new_node1.previous = in_node

		# Add o novo nó
		new_node2.string = string
		new_node2.prefix = new_string
		new_node2.is_leaf = True
		new_node2.keys.append(key)

		in_node.is_leaf = False
		in_node.next.append(new_node2)
		new_node2.previous = in_node

	# Funçao que percorre toda a arvore
	# alocando o indice para cada nó
	def fix_idx(self):
		q = []
		q.append(self.root)
		cnt = 0
		while(q):
			s = q.pop(0)
			s.idx = cnt
			cnt += 1
			for x in s.next:
				q.append(x)
		self.size = cnt
	
	def print(self):
		self._print(self.root)

	def _print(self, node):
		print(node)
		
		for nxt in node.next:
			print('\t', nxt)
		
		for nxt in node.next:
			self._print(nxt)

	def encode(self, f_out):
		self._bfs(self.root, f_out)

	# Um bfs para codificar os nós da Trie
	def _bfs(self, node, f_out):
		visited = [False] * (self.size + 1)
		q = []
		q.append(node)
		visited[node.idx] = True
		cnt = 1
		while q:
			s = q.pop(0)
			if s.previous is not None:
				out = "(" + str(s.previous.idx)

				if s.prefix == '"' or '"' in s.prefix:
					out += ",'" + s.prefix + "') "
				else:
					out += ",\"" + s.prefix + "\") "
				
				for keys in s.keys:
					out += str(hex(keys).split('x')[-1]) + " "
				f_out.write(out)
				f_out.write("\n")
				cnt += 1
			for x in s.next:
				if visited[x.idx] == False:
					q.append(x)
					visited[x.idx] = True