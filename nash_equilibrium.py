import nashpy as nash
import numpy as np

'''strategies: stay or leave'''

A = np.array([
    [5,0],
    [0,0]
    ])

B = np.array([
    [3,0],
    [0,0]])

game = nash.Game(A,B)
equilibria = game.support_enumeration()

for eq in equilibria:
    print(f"NE: {eq}")