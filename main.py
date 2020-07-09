import snap
import numpy as np
import matplotlib.pyplot as plt

np.random.seed()

def TPI(G, threshold):
    s = {v.GetId(): 0 for v in G.Nodes()}
    delta = {v.GetId(): v.GetDeg() for v in G.Nodes()}
    k = {key: value for key, value in threshold.items()}
    neighbours = {v.GetId(): {v.GetNbrNId(i) for i in range(0, v.GetDeg())} for v in G.Nodes()}

    U = {v.GetId() for v in G.Nodes()}

    while U:
        for v in U:
            if k[v] > delta[v]:
                s[v] = s[v] + k[v] - delta[v]
                k[v] = delta[v]

                if k[v] == 0:
                    U.remove(v)

                break
        else:
            tmp = {u: (k[u] * (k[u] + 1)) / (delta[u] * (delta[u] + 1)) for u in U}
            v = max(tmp, key=tmp.get)

            for u in neighbours[v].copy():
                delta[u] = delta[u] - 1
                neighbours[u].remove(v)

            U.remove(v)
    return s

def deferredDecision(G, probs):
    graph = snap.ConvertGraph(snap.PUNGraph, G)
    for e in graph.Edges():
        casualNumber = np.random.uniform()
        src = e.GetSrcNId()
        dst = e.GetDstNId()
        if casualNumber < probs[(src, dst)]:
            graph.DelEdge(src, dst)
    return graph


G = snap.LoadEdgeList(snap.PUNGraph, 'email-Eu-core.txt', 0, 1)

const_x = [i for i in range(1, 10)]
frac_x = [i/10 for i in range(1, 10)]

const_uniform_y = []
const_normal_y = []

frac_uniform_y = []
frac_normal_y = []

uniform_probs = {(e.GetSrcNId(), e.GetDstNId()): np.random.uniform() for e in G.Edges()}
normal_probs = {(e.GetSrcNId(), e.GetDstNId()): 0.5**np.abs(np.random.normal()) for e in G.Edges()}

for i in range(1, 10):
    constant_threshold = {v.GetId(): i for v in G.Nodes()}
    fraction_threshold = {v.GetId(): v.GetDeg()*i/10 for v in G.Nodes()}

    const_uniform_sum = 0
    const_normal_sum = 0
    frac_uniform_sum = 0
    frac_normal_sum = 0

    for j in range(0, 10):
        g_uniform = deferredDecision(G, uniform_probs)
        g_normal = deferredDecision(G, normal_probs)
        
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

    const_uniform_y.append(const_uniform_avg)
    const_normal_y.append(const_normal_avg)
    
    frac_uniform_y.append(frac_uniform_avg)
    frac_normal_y.append(frac_normal_avg)

plt.xlabel('Threshold')
plt.ylabel('Size')

plt.plot(const_x, const_uniform_y, marker='.', label='Uniform probs')
plt.plot(const_x, const_normal_y, marker='.', label='Normal probs')
plt.title('Constant threshold')
plt.legend(title='Probability distribution', loc='upper right', fontsize='small', fancybox=True)
plt.show()

plt.plot(frac_x, frac_uniform_y, marker='.', label='Uniform probs')
plt.plot(frac_x, frac_normal_y, marker='.', label='Normal probs')
plt.title('Degree proportional threshold')
plt.legend(title='Probability distribution', loc='upper right', fontsize='small', fancybox=True)
plt.show()
