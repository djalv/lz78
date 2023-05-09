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
		#s = self.prefix + " " + self.string + " " + str(self.is_leaf) + " "
		s = self.prefix + " "
		s += str(self.idx)
		#if self.previous is None:
			#s += str(None)
		#else:
			#s += self.previous.prefix
		#s = self.prefix + " " + str(self.previous.prefix)
		#s = self.prefix
		
		for keys in self.keys:
			#s += str(hex(keys).split('x')[-1]) + " "
			#s += str(keys) + " "
			pass
		
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

		path = self.search(string)
		in_node = path[-1]

		string_sufix = string
		path_prefix = ""
		
		for n in path:
			max_prefix = longest_prefix(path_prefix, string)
			if max_prefix > 0:
				string_sufix = string_sufix[max_prefix:]
			
			path_prefix += n.prefix
		
		if path_prefix == string:
			if in_node.is_leaf:
				in_node.keys.append(key)
			else:
				for leaf in in_node.next:
					if leaf.prefix == '*':
						leaf.keys.append(key)
			return

		
		max_prefix = longest_prefix(path_prefix, string)
		new_string = string[max_prefix:]

		if new_string == "":
			new_string = '*'
			#print("*", string)
		split = False
		if len(in_node.prefix) > 1:
			split = True

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
			#print(new_node1, in_node)

		new_node2.string = string
		new_node2.prefix = new_string
		new_node2.is_leaf = True
		new_node2.keys.append(key)

		in_node.is_leaf = False
		in_node.next.append(new_node2)
		new_node2.previous = in_node


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

	def _bfs(self, node, f_out):
		visited = [False] * (self.size + 1)
		q = []
		q.append(node)
		visited[node.idx] = True
		cnt = 1
		while q:
			#print(cnt)
			s = q.pop(0)
			if s.previous is not None:
				out = "(" + str(s.previous.idx) + "," + s.prefix + ") "
				
				for keys in s.keys:
					out += str(hex(keys).split('x')[-1]) + " "
				f_out.write(out)
				f_out.write("\n")
				#print(str(cnt) + " (" + str(s.previous.idx) + "," + s.prefix + ")")
				cnt += 1
			for x in s.next:
				if visited[x.idx] == False:
					q.append(x)
					visited[x.idx] = True
'''
with open(sys.argv[1], 'r') as f:
    f_out = open(sys.argv[2], 'w')
    t = Patricia()
    cnt = 0

    for line in f:
        words = line.strip().split()
        for word in words:
        	#print(word, cnt)
        	t.insert(word, cnt)
        	cnt += 1
    t.print(f_out)

#print("longest prefix = ", longest_prefix("estrada", "cheia"))
        
'''
'''
t = Trie()

t.insert("bear",0)
t.insert("bell",1)
t.insert("bid",2)
t.insert("bull",3)
t.insert("sell",4)
t.insert("stock",5)
t.insert("stop",6)
#print(t.size)
#t.print()

t.bfs()
#p = t.search_key(8)
#print(p.string)
'''