import pandas as pd

import evo
import orderbook
import json
import random as rnd
import pprint as pp

"""

Solution data structure:

Each solution is a tuple, with a list of order numbers, and an orderBook dict 
that stores data associated to each order:

([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], orderBook)

---> our goal is to place these in the best possible order
 
Order data stored in an order book dictionary, that is its own class, called orderbook.

orderbook.orderBook looks like:

{
order_id (int) = {
                    priority = Bool,
                    order_quantity = int,
                    product_code = int
                  },
     
order_id (int) = {
                    priority = Bool,
                    order_quantity = int,
                    product_code = int
                  },
     etc...
            }
            
-----------
            
Scoring func: setups

def setups(l, orderBook):
    
    codes = [orderBook[order][product_code] for order in l]
        
    return [1 for t in [(codes[i], codes[i+1]) for i in range(len(codes)-1)]].sum()
    
    
        codes: [X, Z, A, A, B, Z, Z, A, X, X]
        tuples: [(X, Z), (Z, A), (A, A), (A, B), etc...]
        setups: [1,       1,             1,      ....].sum() = 3
        

        
Scoring func: lowPriority

Scoring func: delays
"""


def setups(t):

    l, orderBook = t[0], t[1]
    codes = [orderBook[order]['product_code'] for order in l]
    result = sum([1 for t in [(codes[i], codes[i + 1]) for i in range(len(codes) - 1)] if t[0] != t[1]])
    return result


def lowPriority(t):

    """ Go through order list until hitting final high priority order

        Add to counter of quantities"""

    l, orderBook = t[0], t[1]

    priorityValues = [orderBook[orderNum]['priority'] for orderNum in l]
    # print(priorityValues)

    return sum([orderBook[orderNum]['order_quantity']
                for orderNum in l
                if not priorityValues[orderNum-1] and not sum(priorityValues[orderNum:]) == 0])


def delays(t):

    """ For each order in t[0]      <-----  [6,2,3,89,4,5,7]
            check if t[0][i] > t[0][i+1]
            then counter += orderBook[t[0][quantity]]

    [1, 2, 4, 3]

    """

    l, orderBook = t[0], t[1]
    counter = 0

    for i in range(len(l))[1:]:
        curr_order = l[i]
        prev_order = l[i-1]


        if curr_order < prev_order:
            counter += orderBook[curr_order]['order_quantity']

    return sum([orderBook[l[i]]['order_quantity'] for i in range(len(l))[1:] if l[i] < l[i-1]])


def swapper(solutions):
    """ Agent: Swap two random values """
    L = solutions[0][0]
    i = rnd.randrange(0, len(L))
    j = rnd.randrange(0, len(L))
    L[i], L[j] = L[j], L[i]
    return (L, solutions[0][1])


def agent1(solutions):
    """ Agent: """

def collection(pop):
    """ collects all the data and creates a data frame
    setup, priority, delays
    key = tuple of tuples
    - string of "fitness func" and then score
    - setup = 1st tuple
    - priority score = 2nd tuple
    - delay = 3rd tuple


    key_list = [pop.keys()]
    results = defa{} #make a default dictionary
    for result in key_list:
        if result[0] = "setups"
            add results

        {"Setups": key_list["setups"],
                "Priority Score": key_list["lowPriority"],
                "Delay": key_list["delays"]}
    #df = pd.DataFrame(data = key_dict)
    #print(df)
    print(results)

    """
    key_list = [pop.keys()]
    final_list =[]
    for s in key_list:
        new_dict = {}
        new_dict["setups"] = list(s)[0:]
        new_dict['lowPriority'] = list(s)[1:]
        new_dict['delays'] = list(s)[2:]
        final_list.append(new_dict)
    print(final_list)
    #data_final = pd.DataFrame(data = final_list)
    #print(data_final)
    #make the seaborn pair plot
def main():
    # Create environment
    E = evo.Evo()

    # Create the initial order book
    with open('orders.json') as json_file:
        order_data = json.load(json_file)

    """ NOTE: This framework uses an orderbook object to simulate that possibility of adding and 
              removing orders, as they would be at a real life factory. This makes the code more generalized,
              and more useful.
    """
    O = orderbook.Orderbook()

    for k, v in order_data.items():

        if v['priority'] == "HIGH":
            priority = 1
        else:
            priority = 0

        order_quantity = v['quantity']
        product_code = v['product']

        O.add_order(priority, order_quantity, product_code)

    #pp.pprint(O.orderBook)

    # pp.pprint(O.orderBook)

    # Register fitness criteria
    E.add_fitness_criteria("setups", setups)
    E.add_fitness_criteria("lowPriority", lowPriority)
    E.add_fitness_criteria("delays", delays)

    # Register agents

    E.add_agent("swapper", swapper, 1)

    # Add initial solution
    T = (list(O.orderBook.keys()), O.orderBook)
    E.add_solution(T)
    # print(E)

    # Run the evolver

    # def (n=1, dom=100, status=100):
    E.evolve(1000, 100, 100)

    collection(E.pop)

    # print(f'setups: {setups(T)}')
    # print(f'lowPriority: {lowPriority(T)}')
    # print(f'delay: {delays(T)}')

if __name__ == '__main__':
    main()

