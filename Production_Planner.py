import evo
import orderbook
import json
import random as rnd
import pprint as pp

"""

Solution data structure:

Each solution is a tuple of unique order id's:

([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], orderBook)

---> our goal is to place these in the best possible order
 
Order data stored in an order book dictionary, 
    possible storage locations: 
        - gets defined in main
        - an order book class (more accurate to real world)
        - internally in Evo

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
    print(l)

    codes = [orderBook[order]['product_code'] for order in l]
    return sum([1 for t in [(codes[i], codes[i + 1]) for i in range(len(codes) - 1)] if t[0] != t[1]])


def lowPriority(input):
    pass


def delays(input):
    pass


def swapper(solutions):
    """ Agent: Swap two random values """
    L = solutions[0][0]
    i = rnd.randrange(0, len(L))
    j = rnd.randrange(0, len(L))
    L[i], L[j] = L[j], L[i]
    return (L, solutions[0][1])


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



    # pp.pprint(O.orderBook)

    # Register fitness criteria
    E.add_fitness_criteria("setups", setups)
    # E.add_fitness_criteria("lowPriority", lowPriority)
    # E.add_fitness_criteria("delays", delays)

    # Register agents

    E.add_agent("swapper", swapper, 1)

    # Add initial solution
    T = (list(O.orderBook.keys()), O.orderBook)
    E.add_solution(T)
    # print(E)

    # Run the evolver
    E.evolve(100000, 500, 10000)

    print(setups(T))

if __name__ == '__main__':
    main()
