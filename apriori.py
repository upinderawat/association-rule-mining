import sys
import os
import itertools
from collections import defaultdict

D = list()
l_k = defaultdict(int)
l_pk = defaultdict(int)

def prettyPrint(l_k):
	print("Itemset:  support_cnt")
	print(l_k)

def findSubset(c_k, transaction):
	"""
		find the subset of c_k in transaction
		and updates the count in c_k
		:params
		:returns
	"""
	for itemset in c_k.keys():
		if( set(itemset).issubset(transaction)):
			c_k[itemset]+=1


def apriori_gen(l_pk):
	"""
		:params
		:returns
	"""
	c_k = defaultdict(int)
	for item1 in l_pk:
		for item2 in l_pk:
			if item1[:-1] == item2[:-1] and item1[-1] < item2[-1]:
				c = item1[:-1] + (item1[-1], item2[-1])
				#apriori property
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
		with open(sys.argv[1], 'r') as f:
			for line in f.readlines():
				transaction = line.split()
				D.append(tuple(transaction))
	except Exception as e:
		print("Error: File {} not found", argv[1])

	l_k = find_frequent_1_itemset(D)
	k = 2
	while l_k :
		l_pk = l_k
		c_k = apriori_gen(l_k)
		for transaction in D:
			findSubset(c_k, transaction)
		l_k = {k: v for k,v in c_k.items() if v >= min_sup}
	prettyPrint(l_pk)

if __name__ == '__main__':
	main()