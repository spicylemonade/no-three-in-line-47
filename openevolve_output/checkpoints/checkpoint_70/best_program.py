# initial_program.py

import random

# EVOLVE-BLOCK-START
def run_search():
    n = 47
    # all grid points
    grid = [(x,y) for x in range(n) for y in range(n)]
    S = []
    random.shuffle(grid)
    for (x,y) in grid:
        # check collinearity against every pair already in S
        is_collinear = False
        if len(S) > 0:
            x_last, y_last = S[-1]

            for x1, y1 in S[:-1]:
                if x_last - x1 == 0:
                    slope1 = float('inf')
                else:
                    slope1 = (y_last - y1) / (x_last - x1)
                
                if x - x_last == 0:
                    slope2 = float('inf')
                else:
                    slope2 = (y - y_last) / (x - x_last)
                    
                if abs(slope1 - slope2) < 1e-9:
                    is_collinear = True
                    break

        if not is_collinear:
            S.append((x,y))
    print(len(S))
    return S
# EVOLVE-BLOCK-END 