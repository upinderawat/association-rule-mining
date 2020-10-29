import time

def Load_data(filename):
    with open(filename) as f:
        data_content = f.readlines()

    data_content = [x.strip() for x in data_content]
    # print(content)
    data_content1 = [x.strip() for x in data_content]
    Transaction = []
    transaction_val = 0
    for i in range(0, len(data_content)):
        transaction_val+=1
        Transaction.append(data_content[i].split())
    # print(Transaction)
    total_transactions = transaction_val
    return Transaction

def create_initialset(dataset):
    retDict = {}
    retTreePart = []
    for transaction in dataset:
        retTreePart.append(transaction)
        retDict[frozenset(transaction)] = 1
    return retDict

class TreeNode:
    def __init__(self, Node_name,counter,parentNode=None):
        self.name = Node_name
        self.count = counter
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}
        
    def increment_counter(self, counter):
        self.count += counter

    def display(self, index=1):
        print ('  '*index, self.word, ' ', self.count)
        for child in self.children.values():
            child.display(index+1)

def deletion_hashkey(HashTable, min_support):
  for item in list(HashTable):
    if HashTable[item] < min_support:
      del(HashTable[item])
  return HashTable

def format_HashTable(HeaderTable):
  for k in HeaderTable:
    HeaderTable[k] = [HeaderTable[k], None]
  return HeaderTable

def help_updateTree(dataSet, freq_items, HashTable, return_tree):
    localT = {}
    for tran_set , count in dataSet.items():
        transtn_freq = {}
        for item in tran_set:
            if item in freq_items:
                transtn_freq[item] = HashTable[item][0]
                localT[item] = HashTable[item][1]
        tran_freq_len = len(transtn_freq)
        if tran_freq_len > 0:
            items_ordered = [x[0] for x in sorted(transtn_freq.items(), key=lambda p: p[1], reverse=True)]
            updateTree(items_ordered, return_tree, HashTable, count)
    return return_tree, HashTable

def create_FPTree(dataSet, min_support=2):
  HashTable = {}
  for transaction in dataSet:
    for item in transaction:
      hash_value = HashTable.get(item, 0)
      transaction1 = dataSet[transaction]
      HashTable[item] = hash_value + transaction1

  HashTable = deletion_hashkey(HashTable, min_support)
  item_count = 0
  freq_items = set(HashTable.keys())
  freq_items_length = len(freq_items)
  if(freq_items_length==0):
    return None, None

  HashTable = format_HashTable(HashTable)
  return_tree = TreeNode('Null set', 1)
  item_count += 1
  word_count = item_count
  ret_tree , HashTable= help_updateTree(dataSet, freq_items, HashTable, return_tree)
  return ret_tree, HashTable

def updateTree(itemset, FPTree, HeaderTable, count):
    item_count = 0
    if itemset[0] in FPTree.children:
        item_count += 1
        FPTree.children[itemset[0]].increment_counter(count)
        word_count = count
    else:
        FPTree.children[itemset[0]] = TreeNode(itemset[0], count, FPTree)
        item_count += 1
        word_count = count
        if HeaderTable[itemset[0]][1] == None:
            prev_item = HeaderTable[itemset[0]][1]
            HeaderTable[itemset[0]][1] = FPTree.children[itemset[0]]
            word_count += 1
        else:
            prev_item = HeaderTable[itemset[0]][1]
            update_NodeLink(HeaderTable[itemset[0]][1], FPTree.children[itemset[0]])
    # HeaderTable1 = format_HashTable(HashTable)
    if len(itemset) > 1:
        itemset1 = itemset[1::]
        updateTree(itemset[1::], FPTree.children[itemset[0]], HeaderTable, count)
        word_count = count

def update_NodeLink(Test_Node, Target_Node):
    freq_count1 = Target_Node.count
    freq_count2 = Test_Node.count
    while (Test_Node.nodeLink != None):
        Test_Node = Test_Node.nodeLink
        prev_Node = Test_Node
    Test_Node.nodeLink = Target_Node

def FPTree_uptransveral(leaf_Node, prefixPath):
 freq_count_leafNode = leaf_Node.count
 if leaf_Node.parent != None:
    prefixPath.append(leaf_Node.name)
    freq_count_leafNode += 1
    FPTree_uptransveral(leaf_Node.parent, prefixPath)

def find_prefix_path(basePat, TreeNode):
 Conditional_patterns_base = {}
 freq_items = []
 parent_TreeNode = TreeNode.parent
 word_count = TreeNode.count
 nextNode = TreeNode.nodeLink
 while TreeNode != None:
    prefixPath = []
    word_count += 1
    FPTree_uptransveral(TreeNode, prefixPath)
    nextNode = TreeNode.nodeLink
    if len(prefixPath) > 1:
        Conditional_patterns_base[frozenset(prefixPath[1:])] = TreeNode.count
    TreeNode = TreeNode.nodeLink
    nextNode = TreeNode
 return Conditional_patterns_base


def Mine_Tree(FPTree, HeaderTable, minSupport, prefix, frequent_itemset):
    hashTable_items = HeaderTable.items()
    bigL = [v[0] for v in sorted(HeaderTable.items(),key=lambda p: p[1][0])]
    freq_set = []
    item_count =0
    word_count =0
    parent_Node =None
    for basePat in bigL:
        new_frequentset = prefix.copy()
        new_frequentset.add(basePat)
        # freq_set.append(basePat)
        frequent_itemset.append(new_frequentset)
        freq_set = new_frequentset
        Conditional_pattern_bases = find_prefix_path(basePat, HeaderTable[basePat][1])
        item_count +=1
        Conditional_FPTree, Conditional_header = create_FPTree(Conditional_pattern_bases,minSupport)
        
        if Conditional_header != None and item_count:
            word_count +=1
            Mine_Tree(Conditional_FPTree, Conditional_header, minSupport, new_frequentset, frequent_itemset)


print("Enter the filename:")
filename = input()
print("Enter the minimum support count:")
min_Support = int(input())

initSet = create_initialset(Load_data(filename))
start = time.time()
FPtree, HeaderTable = create_FPTree(initSet, min_Support)

frequent_itemset = []
#call function to mine all ferquent itemsets
Mine_Tree(FPtree, HeaderTable, min_Support, set([]), frequent_itemset)
end = time.time()

print("Time Taken is:")
print(end-start)
print("All frequent itemsets:")
print(frequent_itemset)