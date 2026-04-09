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
    current_node_array = []
    other_node_array = []
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
            # print(g.neighbors(node, mode="in"))
            received[neighbor] += 1
            total_messages += 1
            # print(f"Node {node.index} sends message to Node {neighbor}")
            edge = g.get_eid(neighbor, node.index)
            if lowest[neighbor] == lowest[node.index]:
                yes_array_nodes[node.index] += 1
                yes_array_edges[edge] = True
            else:
                yes_array_edges[edge] = False
                current_node_array.append(node.index)
                other_node_array.append(neighbor)
                # print(f"Node {neighbor} sends message to Node {node.index} on edge {edge}")
                # print(f"Node {node.index} sends message to Node {edge}")
                # edge_test = g.es[edge]
                # print(edge_test)
                # if edge.source == node.index:
                # print(edge_test.target)
                # else:
                # print(edge_test.source)
                # print(f"Edge {edge} is deleted, this is between Node {neighbor} and Node {node.index}")
                # print(f"Edge {edge}: Source {g.es[edge].source} -> Target {g.es[edge].target}")
                # g.delete_edges(edge)
                # g.add_edges([(node.index, neighbor)])
                # edge = g.get_eid(node.index, neighbor)
                # print(f"Edge {edge} is added, this is between Node {node.index} and Node {neighbor}")
                # print(f"Edge {edge}: Source {g.es[edge].source} -> Target {g.es[edge].target}")
            if received[neighbor] == len(g.vs[neighbor].out_edges()):
                q.append(g.vs[neighbor])
        # print(yes_array)
        # for i in range(len(yes_array)):
        #     if yes_array[i] == False:
        #         print(i)
    # print(current_node_array)
    # print(other_node_array)
    # print(yes_array_edges)
    # print(yes_array_nodes)

    
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
                        # print(f"Node {i} has only one incoming edge left, stopping further deletions for this node. edge {edge} is deleted, this is between Node {neighbor} and Node {node.index}")
                        break

    # print(current_node_array)
    # print(other_node_array)
    # print(yes_array_edges)
    # print(yes_array_nodes)

    num_of_deleted = 0
    for i in range(len(yes_array_edges)):
        if yes_array_edges[i] == False:
            edge = g.es[i - num_of_deleted]    # get the Edge object
            source = edge.source      # source vertex index
            target = edge.target      # target vertex index
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
    #     node = g.vs[node_id]
    #     neighbors = []
        
    #     # Get edges connected to this node
    #     edges = node.incident(mode=mode)  # "in", "out", or "all"
        
    #     for edge_id in edges:
    #         edge = g.es[i]
    #         neighbor = get_neighbor_from_edge(g, edge_id, node_id)
    #         neighbors.append(neighbor)

    #     if yes_array[i] == False:
    #         g.delete_edges(i)
    # for e in g.es:
    #     print(f"Edge {e.index}: Source {e.source} -> Target {e.target}")
    # print(yes_array)
    # print(str(total_messages) + "yo_up")
    # fig, ax = plt.subplots()
    # ig.plot(
    #     g,
    #     target=ax,
    #     layout="sugiyama",
    #     vertex_size=15,
    #     vertex_color="grey",
    #     edge_color="#222",
    #     edge_width=1,
    #     vertex_label=[str(i) for i in range(g.vcount())],
    # )
    # plt.show()
    
    if g.vcount() == 1:
        return total_messages
    return total_messages + yo_down(g)

def yo_down(g):
    if g.vcount() == 1:
        return 0
    # Simulate message passing through edges
    # Sources (nodes with outgoing edges but no incoming) initiate messages
    # Other nodes wait for messages from all incoming edges before sending
    total_messages = 0
    received = [0] * g.vcount()  # Track messages received per node
    recieved_from = [float('inf')] * g.vcount()  # Track lowest message received per node
    lowest = [float('inf')] * g.vcount()  # Track lowest message received per node
    q = deque()  # Queue for nodes ready to send messages

    # Identify and enqueue source nodes
    sources = []
    for i in g.vs:
        # print(f"Node {i.index}: in_edges={len(i.in_edges())}, out_edges={len(i.out_edges())}")
        if len(i.in_edges()) == 0 and len(i.out_edges()) > 0:
            sources.append(i)
            lowest[i.index] = i.index  # Initialize lowest with the node's own index for source nodes
            # print(f"Node {i.index} initiates message (source node)")
    # sources = [i for i in g.vs if g.vs[i].in_edges() == 0 and g.vs[i].out_edges() != 0]
    for s in sources:
        q.append(s)
        # print(f"Node {s.index} initiates message (source node)")

    # Process nodes in topological order
    while q:
        node = q.popleft()
        
        # Send message to all outgoing neighbors
        for neighbor in g.neighbors(node, mode="out"):
            # print(f"Node {node.index} sends message to Node {neighbor}")
            received[neighbor] += 1
            total_messages += 1
            if lowest[neighbor] > lowest[node.index]:
                lowest[neighbor] = lowest[node.index]
            # print(f"Node {neighbor} has received {received[neighbor]} messages")
            # If this neighbor has received messages from all incoming edges, enqueue it
            # print(received[neighbor])
            # print(len(g.vs[neighbor].in_edges()))
            if received[neighbor] == len(g.vs[neighbor].in_edges()):
                # print("this is working")
                q.append(g.vs[neighbor])

    # print(f"\nMessage passing simulation complete. Total messages sent: {total_messages}")
    # for i in g.vs:
    #     print(f"Node {i.index}: Lowest message received = {lowest[i.index]}")
    # After creating your graph g...

    # Iterate through all nodes and get edge information
    for v in g.vs:
        # print(f"Node {v.index}:")
        
        # Outgoing edges (edges where this node is the source)
        out_edges = v.out_edges()
        # print(f"  Outgoing edges: {len(out_edges)}")
        # for e in out_edges:
            # print(f"    -> Target: {e.target}, Edge index: {e.index}")
        
        # Incoming edges (edges where this node is the target)
        # in_edges = v.in_edges()
        # print(f"  Incoming edges: {len(in_edges)}")
        # for e in in_edges:
        #     print(f"    <- Source: {e.source}, Edge index: {e.index}")
        
        # print()  # Blank line for readability
        # print(lowest)
    # print(str(total_messages) + "yo_down")
    return total_messages + yo_up(g, lowest)

# random.seed(42)
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

# g = generate_dag(15, 15)
# fig, ax = plt.subplots()
# ig.plot(
#     g,
#     target=ax,
#     layout="sugiyama",
#     vertex_size=15,
#     vertex_color="grey",
#     edge_color="#222",
#     edge_width=1,
#     vertex_label=[str(i) for i in range(g.vcount())],
# )
# plt.show()
# print(list(range(g.ecount())))
# for e in g.es:
    # print(f"Edge {e.index}: Source {e.source} -> Target {e.target}")
# print(yo_down(g))

yplot = []
yplot2 = []
xplot = []
xplot2 = []

# simplified speeds up the code by using the averages from previous runs. Setting simplified to False will make the program take longer but it will then generate new graphs to create new data
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
plt.show()
plt.scatter(xplot2, yplot2, label="m = 2n")
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

#links
#https://python.igraph.org/en/main/index.html 