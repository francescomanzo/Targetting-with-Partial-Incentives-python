import snap
import numpy as np

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


G = snap.LoadEdgeList(snap.PUNGraph, 'email-Eu-core.txt', 0, 1)
threshold = {v.GetId(): np.random.uniform(0, 10) for v in G.Nodes()}
s = TPI(G, threshold)

active = []
active.append({key for key, value in s.items() if value >= threshold[key]})

print(active)
