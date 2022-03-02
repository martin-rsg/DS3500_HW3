"""
Created on Sun Nov  1 20:28:22 2020

@author: rachlin
@file: sorting_v3.py
@description: Sort numbers using evolutionary computing 

Rewritten to use version4 of the evo framework (evo_v4.py)
"""

import evo
import random as rnd


def stepsdown(L):
    """ Objective: Count total magnitude of steps down (larger to smaller value) """
    return sum([x - y for x,y in zip(L, L[1:]) if y < x])


def sumratio(L):
    """ Ratio of sum of first-half values to 2nd half values """
    sz = len(L)
    return round(sum(L[:sz//2]) / sum(L[sz//2+1:]), 5)


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
    E.add_fitness_criteria("stepsdown", stepsdown)
    E.add_fitness_criteria("sumratio", sumratio)

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
