import ciw
#import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from parameters import dict_arrivals, dict_services, dict_routing

network = ciw.create_network(
    arrival_distributions=dict_arrivals,
    service_distributions=dict_services,
    routing=dict_routing,
    priority_classes={'Product_A': 1, 'Product_B': 1, 'maint': 0,},
    number_of_servers=[1, 1, 1, 1]
)

ciw.seed(1)
SIMULATION = ciw.Simulation(network)
SIMULATION.simulate_until_max_time(60*8*5)
recs = pd.DataFrame(SIMULATION.get_all_records())
recs.to_csv('simulation_records.csv', index=False)