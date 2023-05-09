def longest_prefix(P, T):
	n = len(P)
	m = len(T)
	k = 0
	
	while k < n and k < m:
		if P[k] != T[k]:
			break
		k += 1
	return len(P[:k])

