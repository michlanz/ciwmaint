# ciwmaint
DES maintenance model w CIW library (python)

In this first example, we construct a network with:
- 4 machines in series, each with an MTTF of radq(i+1)*100 minutes and an MTTR of 10/(i+1) minutes
- 2 product classes at priority 1 (FIFO):
    ° “Product A” has an exponential service time of (2 i / 3 + 2) minutes and an interarrival every 45 minutes. Its machine routing is [2, 3, 0, 1].
    ° “Product B” has an exponential service time of (3 i / 2 + 1) minutes and an interarrival every 50 minutes. Its machine routing is [0, 1, 2, 3].
- 1 “maintenance” entity class at priority 0 (nonpreemptive), with the parameters defined above

The values plotted are:
… (TBD)

While writing the example, I realized that structuring maintenance events this way gives us no control over the resources (people) available for maintenance. Tomorrow I’ll think about how to build an example that can assess resource utilization.