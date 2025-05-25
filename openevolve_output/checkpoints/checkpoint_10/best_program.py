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
        ok = True
        # check collinearity against every pair already in S
        for i in range(len(S)):
            x1,y1 = S[i]
            for j in range(i+1, len(S)):
                x2,y2 = S[j]
                # collinear iff (y2-y1)*(x - x1) == (y - y1)*(x2 - x1)
                if (y2 - y1)*(x - x1) == (y - y1)*(x2 - x1):
                    ok = False
                    break
            if not ok:
                break
        if ok:
            S.append((x,y))
    print(len(S))
    return S
# EVOLVE-BLOCK-END 