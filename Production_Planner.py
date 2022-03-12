import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import evo
import orderbook
import json
import random as rnd
import pprint as pp
from collections import defaultdict

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
                        if not priorityValues[orderNum - 1]
                        and not sum(priorityValues[orderNum:]) == 0])


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
        prev_order = l[i - 1]


        if curr_order < prev_order:
            counter += orderBook[curr_order]['order_quantity']

    return sum([orderBook[l[i]]['order_quantity'] for i in range(len(l))[1:] if l[i] < l[i - 1]])


def swapper(solutions):
    """ Agent: Swap two random values """
    L = solutions[0][0]
    i = rnd.randrange(0, len(L))
    j = rnd.randrange(0, len(L))
    L[i], L[j] = L[j], L[i]
    return (L, solutions[0][1])


def setupsAgent(solutions):
    """ Finds groupings of like products, searching for groups of 3.
        Picks a group at random, and selects that product.
        Finds that product eleswhere in the production schedule (that isn't in a block).
        Moves it to the selected block."""

    l, orderBook = solutions[0][0], solutions[0][1]

    # Find blocks of like products, search for blocks of 3+
    products = [orderBook[orderNum]['product_code'] for orderNum in l]
    blockLocations = [i for i in range(len(products)-3) if products[i] == products[i+1] == products[i+2]]

    # pick a random block to focus on, and get which product that is
    focusBlockLocation = rnd.choice(blockLocations)
    focusProduct = products[focusBlockLocation]

    # get list of other indexes at which that product exists
    focusProductLocations = [i for i in range(len(products)) if products[i] == focusProduct]

    # disqualify locations that are within a block
    popList = []
    for i in range(3,len(focusProductLocations)):
        cond1 = focusProductLocations[i - 2] in blockLocations
        cond2 = focusProductLocations[i - 1] in blockLocations
        cond3 = focusProductLocations[i - 0] in blockLocations

        if cond1 or cond2 or cond3:
            popList.append(i)

    for location in sorted(popList, reverse=True):
        del focusProductLocations[location]

    # pick an element from focusProductLocations at random and insert it at the focusBlockLocation
    focusProduct_i = rnd.choice(focusProductLocations)
    l.insert(focusBlockLocation, l[focusProduct_i])

    # remove that element from the list
    if focusProduct_i < focusBlockLocation:
        l.pop(focusProduct_i)
    else:
        l.pop(focusProduct_i+1)

    return (l, solutions[0][1])

def priorityAgent(solutions):
    """ Agent directed at placing low priority agents after the final high priority order
        basic mechanism is to take a random low priority order that is before last high priority order,
        and place it into a random spot after the last high priority order"""

    l, orderBook = solutions[0][0], solutions[0][1]

    priorityValues = [orderBook[orderNum]['priority'] for orderNum in l]

    # loop through priority values backwards to find index value of last high priority order
    for i in reversed(range(len(l))):
        if l[i]:
            lastPriorityIndex = i
            break

    # list of low priority index values for l, before the last high priority order
    lowPriorityIndexValues = [idx for idx in range(len(priorityValues)) if priorityValues[idx] == 0][:lastPriorityIndex]

    # select one at random
    i_LowPriority = lowPriorityIndexValues[rnd.randrange(0, len(lowPriorityIndexValues))]

    # select a random spot after last high priority order
    i_AfterHighPriority = rnd.randrange(lastPriorityIndex, len(l)) + 1

    # insert low priority order after last high priority
    l.insert(i_AfterHighPriority, l[i_LowPriority])
    l.pop(i_LowPriority)

    return (l, solutions[0][1])

def collection(pop):
    """ collects all the data and creates a data frame
    setup, priority, delays
    """
    key_list = [pop.keys()]
    new_dict = {}
    new_dict["Setups"] = []
    new_dict["Priority Score"] = []
    new_dict["Delay"] = []
    for t in key_list[0]:

        for sub_t in t:
            fitnessFunc, score = sub_t[0], sub_t[1]
            if fitnessFunc == "setups":
                new_dict["Setups"].append(score)
            if fitnessFunc == "lowPriority":
                new_dict["Priority Score"].append(score)
            if fitnessFunc == "delays":
                new_dict["Delay"].append(score)

    print(new_dict)

    """
    transforming the data into a data frame
    """
    data_final = pd.DataFrame(data = new_dict)

    """
    plotting the data
    """
    sns.pairplot(data_final)
    plt.show()

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

    E.add_agent("swapper", swapper, 3)
    E.add_agent("priorityAgent", priorityAgent, 3)
    E.add_agent("setupsAgent", setupsAgent, 3)

    # Add initial solution
    T = (list(O.orderBook.keys()), O.orderBook)
    E.add_solution(T)

    # Run the evolver

    # def (n=1, dom=100, status=100):
    E.evolve(50000, 100, 100)

    collection(E.pop)

    # print(f'setups: {setups(T)}')
    # print(f'lowPriority: {lowPriority(T)}')
    # print(f'delay: {delays(T)}')


    # swapper(T)

if __name__ == '__main__':
    main()

