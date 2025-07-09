import ciw
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from parameters import * #esplicita sempre dopo: dict_arrivals, dict_services

network = ciw.create_network(
    arrival_distributions=dict_arrivals,
    service_distributions=dict_services,
    routing={'Baby': [[0.0, 1.0, 0.0],
                      [0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0]],
             'Child': [[0.0, 0.0, 1.0],
                       [0.0, 0.0, 0.0],
                       [0.0, 0.0, 0.0]]
    },
    number_of_servers=[1, 1, 1, 1],
)