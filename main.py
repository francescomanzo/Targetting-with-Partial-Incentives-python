import matplotlib.pyplot as plt
import math, numpy as np
import snap
import pandas as pd

from TPI import TPI
from deferred_decision import deferred_decision

np.random.seed()

G = snap.LoadEdgeList(snap.PUNGraph, 'public_figure_edges.txt', 0, 1)

const_x, frac_x = [], []

const_uniform_y, const_normal_y = [], []
frac_uniform_y, frac_normal_y = [], []

uniform_probs = {(e.GetSrcNId(), e.GetDstNId()): np.random.uniform() for e in G.Edges()}
normal_probs = {(e.GetSrcNId(), e.GetDstNId()): np.random.normal() for e in G.Edges()}

deg = [v.GetDeg() for v in G.Nodes()]
iter = np.mean(deg)
step = 2

for i in range(1, (int) (iter), step):
    constant_threshold = {v.GetId(): i for v in G.Nodes()}
    fraction_threshold = {v.GetId(): v.GetDeg() * i / iter for v in G.Nodes()}

    const_uniform_sum, const_normal_sum = 0, 0
    frac_uniform_sum, frac_normal_sum = 0, 0

    for j in range(0, 10):
        g_uniform = deferred_decision(G, uniform_probs, dist='uniform')
        g_normal = deferred_decision(G, normal_probs, dist='normal')

        s = TPI(g_uniform, constant_threshold)
        active = [key for key, value in s.items() if value >= constant_threshold[key]]
        const_uniform_sum = const_uniform_sum + len(active)

        s = TPI(g_normal, constant_threshold)
        active = [key for key, value in s.items() if value >= constant_threshold[key]]
        const_normal_sum = const_normal_sum + len(active)

        s = TPI(g_uniform, fraction_threshold)
        active = [key for key, value in s.items() if value >= fraction_threshold[key]]
        frac_uniform_sum = frac_uniform_sum + len(active)

        s = TPI(g_normal, fraction_threshold)
        active = [key for key, value in s.items() if value >= fraction_threshold[key]]
        frac_normal_sum = frac_normal_sum + len(active)

    const_uniform_avg = const_uniform_sum / 10
    const_normal_avg = const_normal_sum / 10
    frac_uniform_avg = frac_uniform_sum / 10
    frac_normal_avg = frac_normal_sum / 10

    const_x.append(i)
    frac_x.append(i / iter)

    const_uniform_y.append(const_uniform_avg)
    const_normal_y.append(const_normal_avg)

    frac_uniform_y.append(frac_uniform_avg)
    frac_normal_y.append(frac_normal_avg)

plt.xlabel('Threshold')
plt.ylabel('Size')

plt.plot(const_x, const_uniform_y, marker='.', label='Uniform')
plt.plot(const_x, const_normal_y, marker='.', label='Normal')
plt.title('Constant threshold')
plt.legend(title='Probability distribution', loc='lower right', fontsize='small', fancybox=True)
plt.savefig('constant_plot.png')

fig = plt.figure()


plt.xlabel('Threshold')
plt.ylabel('Size')

plt.plot(frac_x, frac_uniform_y, marker='.', label='Uniform')
plt.plot(frac_x, frac_normal_y, marker='.', label='Normal')
plt.title('Degree proportional threshold')
plt.legend(title='Probability distribution', loc='lower right', fontsize='small', fancybox=True)
plt.savefig('degree_proportional_plot.png')
