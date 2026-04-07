import igraph as ig
import matplotlib.pyplot as plt
import random
from collections import deque

def yo_up(g, lowest):
    total_messages = 0
    received = [0] * g.vcount()
    yes_array = [True] * g.ecount()
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
                yes_array[edge] = True
            else:
                yes_array[edge] = False
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
    print(current_node_array)
    print(other_node_array)
    print(yes_array)
    num_of_deleted = 0
    for i in range(len(yes_array)):
        if yes_array[i] == False:
            edge = g.es[i - num_of_deleted]    # get the Edge object
            source = edge.source      # source vertex index
            target = edge.target      # target vertex index
            g.delete_edges(i - num_of_deleted)
            g.add_edges([(target, source)])
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
    fig, ax = plt.subplots()
    ig.plot(
        g,
        target=ax,
        layout="sugiyama",
        vertex_size=15,
        vertex_color="grey",
        edge_color="#222",
        edge_width=1,
        vertex_label=[str(i) for i in range(g.vcount())],
    )
    plt.show()
    return total_messages

def yo_down(g):
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
    return total_messages + yo_up(g, lowest)

random.seed(42)
while True:
    no_isolated = True
    g = ig.Graph.Erdos_Renyi(n=15, m=20, directed=False, loops=False)
    g.to_directed(mode="acyclic")
    ig.summary(g)
    for v in g.vs:
        if len(v.in_edges()) == 0 and len(v.out_edges()) == 0:
            no_isolated = False
    if no_isolated:
        break




fig, ax = plt.subplots()
ig.plot(
    g,
    target=ax,
    layout="sugiyama",
    vertex_size=15,
    vertex_color="grey",
    edge_color="#222",
    edge_width=1,
    vertex_label=[str(i) for i in range(g.vcount())],
)
plt.show()
# print(list(range(g.ecount())))
# for e in g.es:
    # print(f"Edge {e.index}: Source {e.source} -> Target {e.target}")
print(yo_down(g))








#links
#https://python.igraph.org/en/main/index.html 