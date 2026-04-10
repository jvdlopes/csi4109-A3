import igraph as ig
import matplotlib.pyplot as plt
import random
from collections import deque
import numpy as np

def yo_up(g, lowest):
    total_messages = 0
    received = [0] * g.vcount()
    yes_array_edges = [True] * g.ecount()
    yes_array_nodes = [0] * g.vcount()
    q = deque()
    sinks = []
    for i in g.vs:
        if len(i.out_edges()) == 0 and len(i.in_edges()) > 0:
            sinks.append(i)
    for s in sinks:
        q.append(s)
    while q:
        node = q.popleft()
        for neighbor in g.neighbors(node, mode="in"):
            received[neighbor] += 1
            total_messages += 1
            edge = g.get_eid(neighbor, node.index)
            if lowest[neighbor] == lowest[node.index]:
                yes_array_nodes[node.index] += 1
                yes_array_edges[edge] = True
            else:
                yes_array_edges[edge] = False
            if received[neighbor] == len(g.vs[neighbor].out_edges()):
                q.append(g.vs[neighbor])
    for i in range(len(yes_array_nodes)):
        node = g.vs[i]
        if yes_array_nodes[i] > 1:
            for neighbor in g.neighbors(node, mode="in"):
                edge = g.get_eid(neighbor, node.index)
                if yes_array_edges[edge] == True:
                    g.delete_edges(edge)
                    yes_array_edges.pop(edge)
                    yes_array_nodes[i] -= 1
                    if yes_array_nodes[i] == 1:
                        break
    num_of_deleted = 0
    for i in range(len(yes_array_edges)):
        if yes_array_edges[i] == False:
            edge = g.es[i - num_of_deleted]
            source = edge.source
            target = edge.target
            g.delete_edges(i - num_of_deleted)
            g.add_edges([(target, source)])
            num_of_deleted += 1
    num_of_deleted = 0
    for node in range(len(g.vs)):
        if len(g.vs[node - num_of_deleted].in_edges()) == 1 and len(g.vs[node - num_of_deleted].out_edges()) == 0:
            for edge in g.vs[node - num_of_deleted].in_edges():
                g.delete_edges(edge.index)
            g.delete_vertices(node - num_of_deleted)
            num_of_deleted += 1
    if g.vcount() == 1:
        return total_messages
    return total_messages + yo_down(g)

def yo_down(g):
    if g.vcount() == 1:
        return 0
    total_messages = 0
    received = [0] * g.vcount()
    lowest = [float('inf')] * g.vcount()
    q = deque()
    sources = []
    for i in g.vs:
        if len(i.in_edges()) == 0 and len(i.out_edges()) > 0:
            sources.append(i)
            lowest[i.index] = i.index
    for s in sources:
        q.append(s)
    while q:
        node = q.popleft()
        for neighbor in g.neighbors(node, mode="out"):
            received[neighbor] += 1
            total_messages += 1
            if lowest[neighbor] > lowest[node.index]:
                lowest[neighbor] = lowest[node.index]
            if received[neighbor] == len(g.vs[neighbor].in_edges()):
                q.append(g.vs[neighbor])
    return total_messages + yo_up(g, lowest)


def generate_dag(nodes, edges):
    while True:
        no_isolated = True
        if edges == nodes:
            g = ig.Graph.Tree(n=nodes, children=2)
            while True:
                rand1 = random.randint(0, nodes - 1)
                rand2 = random.randint(0, nodes - 1)
                if rand1 != rand2 and g.are_adjacent(rand1, rand2) == False:
                    g.add_edges([(min(rand1,rand2), max(rand1,rand2))])
                    break
        else:
            g = ig.Graph.Erdos_Renyi(n=nodes, m=edges, loops=False)
        if not g.is_connected():
            continue
        g.to_directed(mode="acyclic")
        ig.summary(g)
        for v in g.vs:
            if len(v.in_edges()) == 0 and len(v.out_edges()) == 0:
                no_isolated = False
        if no_isolated:
            break
    return g

yplot = []
yplot2 = []
xplot = []
xplot2 = []

# simplified speeds up the code by using the averages from previous runs. Turning simplified to false will make the program take longer as it adds a few thousand more runs of the algorithm, but the new data that is generated will be identical to the current constants.
simplified = True


answer_20_1 = 0
for i in range(1000):
    g = generate_dag(20, 20)
    answer_20_1 += yo_down(g)
yplot.append(answer_20_1 / 1000)
xplot.append(20)

m = int(20 * np.log(20))
answer_20_2 = 0
for i in range(1000):
    g = generate_dag(20, m)
    answer_20_2 += yo_down(g)
yplot.append(answer_20_2 / 1000)
xplot.append(20)

m = int(20 * np.sqrt(20))
answer_20_3 = 0
for i in range(1000):
    g = generate_dag(20, m)
    answer_20_3 += yo_down(g)
yplot.append(answer_20_3 / 1000)
xplot.append(20)

m = (20 * (20 - 1)) // 2
answer_20_4 = 0
for i in range(1000):
    g = generate_dag(20, m)
    answer_20_4 += yo_down(g)
yplot.append(answer_20_4 / 1000)
xplot.append(20)

answer_30_1 = 0
for i in range(1000):
    g = generate_dag(30, 30)
    answer_30_1 += yo_down(g)
yplot.append(answer_30_1 / 1000)
xplot.append(30)

answer_30_2 = 0
m = int(30 * np.log(30))
for i in range(1000):
    g = generate_dag(30, m)
    answer_30_2 += yo_down(g)
yplot.append(answer_30_2 / 1000)
xplot.append(30)

answer_30_3 = 0
m = int(30 * np.sqrt(30))
for i in range(1000):
    g = generate_dag(30, m)
    answer_30_3 += yo_down(g)
yplot.append(answer_30_3 / 1000)
xplot.append(30)

answer_30_4 = 0
m = (30 * (30 - 1)) // 2
for i in range(1000):
    g = generate_dag(30, m)
    answer_30_4 += yo_down(g)
yplot.append(answer_30_4 / 1000)
xplot.append(30)

answer_40_1 = 0
for i in range(1000):
    g = generate_dag(40, 40)
    answer_40_1 += yo_down(g)
yplot.append(answer_40_1 / 1000)
xplot.append(40)

answer_40_2 = 0
m = int(40 * np.log(40))
for i in range(1000):
    g = generate_dag(40, m)
    answer_40_2 += yo_down(g)
yplot.append(answer_40_2 / 1000)
xplot.append(40)

answer_40_3 = 0
m = int(40 * np.sqrt(40))
for i in range(1000):
    g = generate_dag(40, m)
    answer_40_3 += yo_down(g)
yplot.append(answer_40_3 / 1000)
xplot.append(40)

answer_40_4 = 3042000
if simplified == False:
    answer_40_4 = 0
    m = (40 * (40 - 1)) // 2
    for i in range(1000):
        g = generate_dag(40, m)
        answer_40_4 += yo_down(g)
yplot.append(answer_40_4 / 1000)
xplot.append(40)

answer_60_1 = 0
for i in range(1000):
    g = generate_dag(60, 60)
    answer_60_1 += yo_down(g)
yplot.append(answer_60_1 / 1000)
xplot.append(60)

answer_60_2 = 0
m = int(60 * np.log(60))
for i in range(1000):
    g = generate_dag(60, m)
    answer_60_2 += yo_down(g)
yplot.append(answer_60_2 / 1000)
xplot.append(60)

answer_60_3 = 0
m = int(60 * np.sqrt(60))
for i in range(1000):
    g = generate_dag(60, m)
    answer_60_3 += yo_down(g)
yplot.append(answer_60_3 / 1000)
xplot.append(60)

answer_60_4 = 6962000
if simplified == False:
    answer_60_4 = 0
    m = (60 * (60 - 1)) // 2
    for i in range(1000):
        g = generate_dag(60, m)
        answer_60_4 += yo_down(g)
yplot.append(answer_60_4 / 1000)
xplot.append(60)

answer_80_1 = 0
for i in range(1000):
    g = generate_dag(80, 80)
    answer_80_1 += yo_down(g)
yplot.append(answer_80_1 / 1000)
xplot.append(80)

answer_80_2 = 0
m = int(80 * np.log(80))
for i in range(1000):
    g = generate_dag(80, m)
    answer_80_2 += yo_down(g)
yplot.append(answer_80_2 / 1000)
xplot.append(80)

answer_80_3 = 0
m = int(80 * np.sqrt(80))
for i in range(1000):
    g = generate_dag(80, m)
    answer_80_3 += yo_down(g)
yplot.append(answer_80_3 / 1000)
xplot.append(80)

answer_80_4 = 12482000
if simplified == False:
    answer_80_4 = 0
    m = (80 * (80 - 1)) // 2
    for i in range(1000):
        g = generate_dag(80, m)
        answer_80_4 += yo_down(g)
yplot.append(answer_80_4 / 1000)
xplot.append(80)

answer_100_1 = 0
for i in range(1000):
    g = generate_dag(100, 100)
    answer_100_1 += yo_down(g)
yplot.append(answer_100_1 / 1000)
xplot.append(100)

answer_100_2 = 0
m = int(100 * np.log(100))
for i in range(1000):
    g = generate_dag(100, m)
    answer_100_2 += yo_down(g)
yplot.append(answer_100_2 / 1000)
xplot.append(100)

answer_100_3 = 0
m = int(100 * np.sqrt(100))
for i in range(1000):
    g = generate_dag(100, m)
    answer_100_3 += yo_down(g)
yplot.append(answer_100_3 / 1000)
xplot.append(100)

answer_100_4 = 19602000
if simplified == False:
    answer_100_4 = 0
    m = (100 * (100 - 1)) // 2
    for i in range(1000):
        g = generate_dag(100, m)
        answer_100_4 += yo_down(g)
yplot.append(answer_100_4 / 1000)
xplot.append(100)

answer2_20_1 = 0
n = 20
m = n * 2
for i in range(1000):
    g = generate_dag(n, m)
    answer2_20_1 += yo_down(g)
yplot2.append(answer2_20_1 / 1000)
xplot2.append(n)

answer2_30_1 = 0
n = 30
m = n * 2
for i in range(1000):
    g = generate_dag(n, m)
    answer2_30_1 += yo_down(g)
yplot2.append(answer2_30_1 / 1000)
xplot2.append(n)

answer2_40_1 = 0
n = 40
m = n * 2
for i in range(1000):
    g = generate_dag(n, m)
    answer2_40_1 += yo_down(g)
yplot2.append(answer2_40_1 / 1000)
xplot2.append(n)

answer2_60_1 = 0
n = 60
m = n * 2
for i in range(1000):
    g = generate_dag(n, m)
    answer2_60_1 += yo_down(g)
yplot2.append(answer2_60_1 / 1000)
xplot2.append(n)

answer2_80_1 = 0
n = 80
m = n * 2
for i in range(1000):
    g = generate_dag(n, m)
    answer2_80_1 += yo_down(g)
yplot2.append(answer2_80_1 / 1000)
xplot2.append(n)

answer2_100_1 = 0
n = 100
m = n * 2
for i in range(1000):
    g = generate_dag(n, m)
    answer2_100_1 += yo_down(g)
yplot2.append(answer2_100_1 / 1000)
xplot2.append(n)

plt.scatter(xplot, yplot, label="m = n, nlogn, nsqrt(n), n^2")
plt.xlabel("number of nodes (n)")
plt.ylabel("average message complexity")
plt.title("Procedure 1:")
plt.show()
plt.scatter(xplot2, yplot2, label="m = 2n")
plt.xlabel("number of nodes (n)")
plt.ylabel("average message complexity")
plt.title("Procedure 2:")
plt.show()


print(f"fixed n = 20 with m = n: {answer_20_1 / 1000}")
print(f"fixed n = 20 with m = nlogn: {answer_20_2 / 1000}")
print(f"fixed n = 20 with m = nsqrt(n):{answer_20_3 / 1000}")
print(f"fixed n = 20 with m = n^2: {answer_20_4 / 1000}")
print(f"fixed n = 30 with m = n: {answer_30_1 / 1000}")
print(f"fixed n = 30 with m = nlogn: {answer_30_2 / 1000}")
print(f"fixed n = 30 with m = nsqrt(n): {answer_30_3 / 1000}")
print(f"fixed n = 30 with m = n^2: {answer_30_4 / 1000}")
print(f"fixed n = 40 with m = n: {answer_40_1 / 1000}")
print(f"fixed n = 40 with m = nlogn: {answer_40_2 / 1000}")
print(f"fixed n = 40 with m = nsqrt(n): {answer_40_3 / 1000}")
print(f"fixed n = 40 with m = n^2: {answer_40_4 / 1000}")
print(f"fixed n = 60 with m = n: {answer_60_1 / 1000}")
print(f"fixed n = 60 with m = nlogn: {answer_60_2 / 1000}")
print(f"fixed n = 60 with m = nsqrt(n): {answer_60_3 / 1000}")
print(f"fixed n = 60 with m = n^2: {answer_60_4 / 1000}")
print(f"fixed n = 80 with m = n: {answer_80_1 / 1000}")
print(f"fixed n = 80 with m = nlogn: {answer_80_2 / 1000}")
print(f"fixed n = 80 with m = nsqrt(n): {answer_80_3 / 1000}")
print(f"fixed n = 80 with m = n^2: {answer_80_4 / 1000}")
print(f"fixed n = 100 with m = n: {answer_100_1 / 1000}")
print(f"fixed n = 100 with m = nlogn: {answer_100_2 / 1000}")
print(f"fixed n = 100 with m = nsqrt(n): {answer_100_3 / 1000}")
print(f"fixed n = 100 with m = n^2: {answer_100_4 / 1000}")
print(f"fixed n = 20 with m = 2n: {answer2_20_1 / 1000}")
print(f"fixed n = 30 with m = 2n: {answer2_30_1 / 1000}")
print(f"fixed n = 40 with m = 2n: {answer2_40_1 / 1000}")
print(f"fixed n = 60 with m = 2n: {answer2_60_1 / 1000}")
print(f"fixed n = 80 with m = 2n: {answer2_80_1 / 1000}")
print(f"fixed n = 100 with m = 2n: {answer2_100_1 / 1000}")

#refrences
#https://python.igraph.org/en/main/index.html 