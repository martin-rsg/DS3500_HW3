

import evo

"""

Solution data structure:

Each solution is a list of unique order id's:

[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

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




def setups(input):
    pass

def lowPriority(input):
    pass

def delays(input):
    pass

def swapper(solutions):
    """ Agent: Swap two random values """
    L = solutions[0]
    i = rnd.randrange(0, len(L))
    j = rnd.randrange(0, len(L))
    L[i], L[j] = L[j], L[i]
    return L


def main():

    # Create environment
    E = evo.Evo()


    # Register fitness criteria
    E.add_fitness_criteria("setups", setups)
    E.add_fitness_criteria("lowPriority", lowPriority)
    E.add_fitness_criteria("delays", delays)

    # Register agents
    E.add_agent("swapper", swapper, 1)

    # Add initial solution
    L = [rnd.randrange(1, 99) for _ in range(20)]
    E.add_solution(L)
    print(E)

    # Run the evolver
    E.evolve(100000, 500, 10000)


if __name__ == '__main__':
    main()