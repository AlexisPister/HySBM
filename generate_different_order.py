import pandas as pd

from generator_v2 import Generator

# This script does simulations to test if the order of node traversal has an effect on th Gini of hyperedges

# Same as df_fits but other format so easier altair plots
df_fits2 = pd.DataFrame()

N_edges = 200
# Last value is the one used for most simulations
Ns = [1000]
p = 0.03
N_graphs = 100
N_coms = 4

df_sims = pd.DataFrame()

frac = 0.4
q = round(p * frac, 4)

community_array = []
for i in range(N_coms):
    community_array += [i for x in range(Ns[0] // N_coms)]

sim_data_list = []
for strat in ["weighted", "max", "min", "frequent"]:
    for order_strat in ["fixed", 'random', "community-order"]:
        for n in Ns:
            for n_graph in range(N_graphs):
                gen = Generator(n, N_edges, N_coms, p, q, community_array, strat)
                gen.run(order_strat)

                #  For com distrib of hyperedges
                comp = gen.hyperedges_nmax()
                ginis = gen.ginis()

                # for fraction in comp:
                # df = pd.DataFrame({"q": [q] * len(comp), "value": comp, "gini": ginis, "N_nodes": [n] * len(comp),
                #                    "strat": [strat] * len(comp), "order": order_strat})
                df = pd.DataFrame({"q": q, "value": comp, "gini": ginis, "N_nodes": n,
                                   "strat": strat, "order": order_strat})
                sim_data_list.append(df)
                # df_sims = pd.concat([df_sims, df])


df_sims = pd.concat(sim_data_list)
# print(df_sims)

fn = f"simulations_nodeOrders/he_distrib_{frac}p_{N_graphs}graphs_{N_edges}edges_orders.csv"
df_sims.to_csv(fn, sep=',', index=False, encoding='utf-8')