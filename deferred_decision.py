import numpy as np
import snap


def deferred_decision(G, probs, dist):
    graph = snap.ConvertGraph(snap.PUNGraph, G)

    for e in graph.Edges():

        if dist == 'uniform':
            x = np.random.uniform()
        else:
            x = np.random.normal()

        src = e.GetSrcNId()
        dst = e.GetDstNId()

        if x < probs[(src, dst)]:
            graph.DelEdge(src, dst)

    return graph
