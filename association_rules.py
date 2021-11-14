import itertools
from fractions import Fraction 

class association_rules(object):

    def __init__(self,iterable):
        data = {}  # dictionary to store the data
        for elem in iterable:
            data[elem[0]] = elem[1]
        self.data = data

    def create_freq_table(self, data:dict) -> dict:

        if data is None:
            data = self.data

        freq_table = {}  # dict
        for value in data.values():
            for elem in value:
                t = (elem,)
                if t in freq_table.keys():
                    freq_table[t] += 1
                else:
                    freq_table[t] = 1

        return freq_table
        

    def generate_next_level(self,itemset):
        '''
        >>> generate_next_level(itemset = (('HotDogs', 'Buns'), ('HotDogs', 'Chips'), ('HotDogs', 'Coke'), ('Chips', 'Coke')))
        {'Coke', 'Chips', 'HotDogs'}
        '''
        if itemset is None:
            return None
        intersections = set()
        for comb in itertools.combinations(itemset,2):
            d = set(comb[0]).intersection(set(comb[1]))
            if d: # make sure d is not empty
                intersections = intersections.union(d)

        return intersections

    def popular_items(self, data:dict, support:int = 0) -> dict:

        freq_table = self.create_freq_table(data)

        itemset = set()
        for key in freq_table.keys():
            if freq_table[key] >= support:
                itemset = itemset.union(set(key))
        
        freq_table = {key:value for (key,value) in freq_table.items() if value >= support}
        k = 2

        while(itemset):
            intersections = set()
            if k > 2:
                for comb in itertools.combinations(itemset,2):
                    d = set(comb[0]).intersection(set(comb[1]))
                    if d: # make sure d is not empty
                        intersections = intersections.union(d)
                itemset = intersections


            freq_itemset = {}
            for comb in itertools.combinations(itemset,k): # k - itemset are itemsets with k elements
                count = 0
                for value in data.values():
                    if set(comb) <= value:  #if it's a subset of the value 
                        count += 1
                if count >= support:
                    freq_itemset[comb] = count
            itemset = tuple(freq_itemset.keys())
            freq_table.update(freq_itemset)
            k += 1
            

        return freq_table



    def freq_all_combinations(self, data:dict) -> dict:
        """
        (list) -> tuple(int, list)
        """

        if data is None:
            data = self.data

        freq_table = {} #dict
        for value in data.values():
            for elem in value:
                if elem in freq_table.keys():
                    freq_table[elem] += 1
                else:
                    freq_table[elem] = 1

        new_freq_table = {(key,):freq_table[key] for key in freq_table}
        sorted_freq_table = dict(sorted(new_freq_table.items()))
        #print(sorted_freq_table)

        no_duplicates = tuple(freq_table.keys())
        #no_duplicates.sort()
        #print(no_duplicates)

        length = len(no_duplicates)
        for i in range(2,length):
            for comb in itertools.combinations(no_duplicates,i):
                count = 0
                for value in data.values():
                    if set(comb) <= value:  #if it's a subset of the value 
                        count += 1
                #new_freq_table[comb] = count
                # remember that set is unhashable
                sorted_freq_table[comb] = count
        
        
        #return new_freq_table
        return sorted_freq_table   


    def create_assocation_rules(self, popular_items:dict, min_conf:float = 0.0):
        associations = dict()  # rules
        for key in popular_items.keys():
            n = len(key)
            if n > 1:
                setA = set(key)
                for integer in range(1, n):
                    for head in itertools.permutations(setA, integer):
                        if head in popular_items.keys(): 
                            confidence = Fraction(
                                popular_items[key], popular_items[head])
                            if confidence >= min_conf:
                                body = setA - set(head)
                                head = tuple(head)
                                body = tuple(body)
                                associations[(head, body,)] = confidence
                                # tuple(head,body,) # do not use [(head,body)]
                                # can also use float(confidence) to convert it to floating point

        print("list of association rules: ")
        for rule in associations:
            head = rule[0]
            tail = rule[1]
            confidence = associations[rule]
            print(f"{head} -> {tuple(tail)} {str(confidence)} = {float(confidence)}", end = " ")
            print()
        return associations

    def __repr__(self) -> str:
        return str(self.data)



def main():

    #run tests here
    #sort by lexigraphical order? 
    #transactions = {"transaction1":{1,3,4}, "transaction2":{2,3,5}, "transaction3":{1,2,3,5}, "transaction4": {2,5} }

    transactions = {'T1': {'HotDogs', 'Buns', 'Ketchup'},
                    'T2': {'HotDogs', 'Buns'},
                    'T3': {'HotDogs', 'Coke', 'Chips'},
                    'T4': {'Chips', 'Coke'},
                    'T5': {'Chips', 'Ketchup'},
                    'T6': {'HotDogs', 'Coke', 'Chips'}}

    n = len(transactions) #number of transactions = 6
    print(f"number of transactions: {n}") 

    d = association_rules({}) # initialize empty object so you can use the methods

    print("popular items:")
    popular_items = d.popular_items(transactions,support = 2)
    print(popular_items)
    print("")

    d.create_assocation_rules(popular_items, min_conf=0.6)
    print()

    

if __name__ == "__main__":
    main()
