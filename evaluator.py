# evaluator.py

import importlib.util
import concurrent.futures
import time

def run_with_timeout(func, timeout_seconds=5):
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
        fut = ex.submit(func)
        return fut.result(timeout=timeout_seconds)

def evaluate(program_path):
    """
    Loads the candidate program, runs run_search(), 
    verifies no three collinear, and returns:
      - point_count: number of unique points
      - overall_score: equal to point_count if valid, else 0
    """
    
    spec = importlib.util.spec_from_file_location("prog", program_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    start_time = time.time()
    pts = [] 
    try:
        pts = run_with_timeout(mod.run_search, timeout_seconds=10)
    except Exception as e:
        print(f"Evaluation error during run_search: {e}")
        return {"point_count": 0.0, "overall_score": 0.0, "runtime": time.time() - start_time, "error": 1.0}

    if not isinstance(pts, list):
        return {"point_count": 0.0, "overall_score": 0.0, "runtime": time.time() - start_time, "error": 1.0}

    
    unique = set(pts)
    point_count = len(unique)

    # check collinearity
    n = 47 
    valid = True
    pts_list = list(unique)
    L = point_count
    for i in range(L):
        x1,y1 = pts_list[i]
        if not (0 <= x1 < n and 0 <= y1 < n):
            valid = False
            break
        for j in range(i+1, L):
            x2,y2 = pts_list[j]
            if not (0 <= x2 < n and 0 <= y2 < n):
                valid = False
                break
            for k in range(j+1, L):
                x3,y3 = pts_list[k]
                if not (0 <= x3 < n and 0 <= y3 < n):
                    valid = False
                    break
                if (y2-y1)*(x3-x1) == (y3-y1)*(x2-x1):
                    valid = False
                    break
            if not valid:
                break
        if not valid:
            break
    
    elapsed_time = time.time() - start_time

    if valid:
        overall = float(point_count)
        if overall > 0: 
             print(f"Valid solution with {point_count} points. Length: N/A (not applicable). Points: {sorted(list(unique))}")
    else:
        overall = -1000.0 
    
    return {
        "point_count": float(point_count),
        "overall_score": overall,
        "runtime": elapsed_time,
        "valid_solution": 1.0 if valid else 0.0 
    } 