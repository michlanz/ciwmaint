import ciw
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Seed the RNG for reproducibility
ciw.seed(42)

# ----------------------
# 0) PARAMETERS
# ----------------------
MEAN_IAT = 5.0    # exponential interarrival mean (minutes)
MEAN_SRV = 6.0    # exponential service mean at node 1 (minutes)
MTTF      = 60.0  # mean time to failure (minutes)
MTTR      = 5.0   # mean time to repair (minutes)
SIM_TIME  = 480.0 # total simulation time = 8 hours = 480 minutes

# probability that a job, upon completing service at node 1, goes to maintenance
p_break = MTTR / (MTTF + MTTR)

# ----------------------
# 1) DEFINE THE NETWORK
# ----------------------
network = ciw.create_network(
    arrival_distributions = [
        ciw.dists.Exponential(rate=1/MEAN_IAT),  # external arrivals only at node 1
        None                                     # no external arrivals at node 2
    ],
    service_distributions = [
        ciw.dists.Exponential(rate=1/MEAN_SRV),  # node 1: production
        ciw.dists.Deterministic(value=MTTR)      # node 2: maintenance repair time
    ],
    number_of_servers = [1, 1],  # one server at each node
    routing = [
        [1 - p_break, p_break],  # from node 1: exit with 1-p_break or go to node 2
        [1.0,       0.0      ]   # from node 2: always return to node 1
    ]
)

# ----------------------
# 2) RUN THE SIMULATION
# ----------------------
sim = ciw.Simulation(network)
sim.simulate_until_max_time(SIM_TIME)

# ----------------------
# 3) COLLECT ALL RECORDS
# ----------------------
recs = sim.get_all_records()

# ----------------------
# 4) COMPUTE RESOURCE TIMES
# ----------------------
# Total busy time at each node = sum of service times
busy1 = sum(r.service_time for r in recs if r.node == 1)
busy2 = sum(r.service_time for r in recs if r.node == 2)

# For production node:
#   - down time = total time spent in maintenance (busy2)
#   - idle time = SIM_TIME − busy1 − down1
down1 = busy2
idle1 = SIM_TIME - busy1 - down1

# For maintenance node:
#   - idle time = SIM_TIME − busy2
idle2 = SIM_TIME - busy2

# ----------------------
# 5) BUILD SUMMARY TABLE
# ----------------------
df_times = pd.DataFrame({
    'Resource': [
        'Production Busy',
        'Production Idle',
        'Production Down',
        'Maintenance Busy',
        'Maintenance Idle'
    ],
    'Time (min)': [
        busy1,
        idle1,
        down1,
        busy2,
        idle2
    ]
})

# Print the table
print(df_times)

# ----------------------
# 6) BUILD INVENTORY OVER TIME
# ----------------------
events = []
for r in recs:
    # When a job arrives to node 1
    events.append((r.arrival_date,    +1))
    # When a job finishes service at either node
    events.append((r.service_end_date, -1))
# sort by event time
events.sort(key=lambda x: x[0])

times  = np.linspace(0, SIM_TIME, int(SIM_TIME) + 1)
counts = []
cur    = 0
idx    = 0
for t in times:
    while idx < len(events) and events[idx][0] <= t:
        cur += events[idx][1]
        idx += 1
    counts.append(cur)

# ----------------------
# 7) PLOT PERCENTAGE HISTOGRAMS
# ----------------------
# 7a) Production percentages
prod_states = ['Busy', 'Idle', 'Down']
prod_times  = [busy1, idle1, down1]
total_prod  = sum(prod_times)
prod_perc   = [t / total_prod * 100 for t in prod_times]

plt.figure()
plt.bar(prod_states, prod_perc)
plt.ylim(0, 100)
plt.xlabel('Production State')
plt.ylabel('Percentage (%)')
plt.title('Production Resource State Distribution')
for i, p in enumerate(prod_perc):
    plt.text(i, p + 1, f"{p:.1f}%", ha='center')
plt.tight_layout()
plt.show()

# 7b) Maintenance percentages
maint_states = ['Busy', 'Idle']
maint_times  = [busy2, idle2]
total_maint  = sum(maint_times)
maint_perc   = [t / total_maint * 100 for t in maint_times]

plt.figure()
plt.bar(maint_states, maint_perc)
plt.ylim(0, 100)
plt.xlabel('Maintenance State')
plt.ylabel('Percentage (%)')
plt.title('Maintenance Resource State Distribution')
for i, p in enumerate(maint_perc):
    plt.text(i, p + 1, f"{p:.1f}%", ha='center')
plt.tight_layout()
plt.show()

# ----------------------
# 8) PLOT INVENTORY LEVEL
# ----------------------
plt.figure()
plt.step(times, counts, where='post')
plt.xlabel('Time (minutes)')
plt.ylabel('Jobs in System')
plt.title('Inventory Level over 8 Hours')
plt.tight_layout()
plt.show()
