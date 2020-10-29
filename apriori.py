import sys
import os
import itertools
from collections import defaultdict
import time

D = list()
l_k = defaultdict(int)
l_pk = defaultdict(int)

def prettyPrint(l_k):
	print("-"*40)
	print("Itemset {:20} support_cnt".format(""))
	print("-"*40)
	for k,v in l_k.items():
		print("{}{:<20}{}".format(k, "", v))
	# print(l_k)

def isSubsetOf(itemset, transaction):
	"""
		find the subset of c_k in transaction
		and updates the count in c_k
		:params
		:returns
	"""
	n, m = len(itemset), len(transaction)
	i = j = 0
	while i < n and j < m:
		if itemset[i] == transaction[j] :
			i +=1
			j+=1
		elif itemset[i] > transaction[j]:
			j+=1
		else:
			break

	return i == n

def all_frequent(c, l_pk):
	"""
	checks whether all subsets of size k-1 in c are frequent in
	l_pk
	"""
	for s in itertools.combinations(c, len(c)-1):
		if not s in l_pk:
			return False
	return True


def apriori_gen(l_pk, use_apiori=False):
	"""
		:params l_pk frequent itemsets of size k-1
		:returns c_k candidate itemsets of size k
	"""
	c_k = defaultdict(int)
	for item1 in l_pk:
		for item2 in l_pk:
			if item1[:-1] == item2[:-1] and item1[-1] < item2[-1]:
				c = item1[:-1] + (item1[-1], item2[-1])
				if use_apiori:
					#apriori property
					if all_frequent(c, l_pk):
						c_k[c] = 0
				else:
					c_k[c] = 0
	return c_k

def find_frequent_1_itemset(D):
	"""
		returns:
		params:
	"""
	for transaction in D:
		for item in transaction:
			l_pk[(item,)] += 1
	return l_pk

def main():

	#validate input
	if len(sys.argv) != 3:
		print("Syntax Error: python apriori.py <transaction_file> <min_sup>")
		return
	try:
		min_sup = int(sys.argv[2])
		if min_sup <=0:
			raise Exception("min_sup can't be negative")
	except ValueError as e:
		print("Error: min_sup must be integer.")
		return
	except Exception as e:
		print(e)
		return

	#read transaction data in D
	try:
		file = sys.argv[1]
		with open(file, 'r') as f:
			for line in f.readlines():
				transaction = line.split()
				D.append(tuple(transaction))
	except Exception as e:
		print("Error: File {} not found", sys.argv[1])

	startTime = time.time()
	l_k = find_frequent_1_itemset(D)
	k = 2
	while l_k :
		print("Processing {} frequent itemset".format(k))
		k+=1
		l_pk = l_k
		c_k = apriori_gen(l_k, use_apiori=False)
		for transaction in D:
			for itemset in c_k.keys():
				if isSubsetOf(itemset, transaction):
					c_k[itemset]+=1
		l_k = {k: v for k,v in c_k.items() if v >= min_sup}
	endTime = time.time()
	prettyPrint(l_pk)
	print("\nFinished in: ", endTime-startTime)

if __name__ == '__main__':
	main()