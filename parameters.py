import ciw
#import pandas as pd
#import numpy as np

#parameters definition ==========================================================================================
interarrival_A = 45
interarrival_B = 50

route_A = [2, 3, 0, 1]
route_B = [0, 1, 2, 3]

num_machines = len(set(route_A+route_B))

MTTF = [100*(i+1)**(1/2) for i in range(num_machines)]
MTTR = [10/(i+1) for i in range(num_machines)]
MTBF = [sum(x) for x in zip(MTTF, MTTR)]

#dictionary definition ==========================================================================================
#WARN approximation about the MTBF for the maintenance in arrival dictionary

#arrivals dictionary
dict_arrivals = {
    'Product_A': [ciw.dists.Exponential(rate=60/interarrival_A) if route_A[0] == i else None for i in range(num_machines)], 
    'Product_B': [ciw.dists.Exponential(rate=60/interarrival_B) if route_B[0] == i else None for i in range(num_machines)],
    'maint' : [ciw.dists.Exponential(rate=60/MTBF[i]) for i in range(num_machines)]
}

#service dictionary
dict_services = {
    'Product_A': [ciw.dists.Exponential(rate=60/(2*i/3 + 2)) for i in range(num_machines)],
    'Product_B': [ciw.dists.Exponential(rate=60/(3*i/2 + 1)) for i in range(num_machines)],
    'maint' : [ciw.dists.Exponential(rate=60/MTTR[i]) for i in range(num_machines)]
}

#routing (maintenance does not have a route) (FLOATS ONLY)
dict_routing = {
    'Product_A' : [[1.0 if (i, j) in list(zip(route_A, route_A[1:])) else 0.0 for j in range(num_machines)] for i in range(num_machines)],
    'Product_B' : [[1.0 if (i, j) in list(zip(route_B, route_B[1:])) else 0.0 for j in range(num_machines)] for i in range(num_machines)],
    'maint' : [[0.0 for _ in range(num_machines)] for _ in range(num_machines)]
}