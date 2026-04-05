import igraph as ig
import matplotlib.pyplot as plt
import random
from collections import deque

g = ig.Graph.Erdos_Renyi(n=15, m=30, directed=False, loops=False)
g.to_directed(mode="acyclic")
ig.summary(g)

# Simulate message passing through edges
# Sources (nodes with outgoing edges but no incoming) initiate messages
# Other nodes wait for messages from all incoming edges before sending
total_messages = 0
received = [0] * g.vcount()  # Track messages received per node
lowest = [float('inf')] * g.vcount()  # Track lowest message received per node
q = deque()  # Queue for nodes ready to send messages

# Identify and enqueue source nodes
sources = []
for i in g.vs:
    print(f"Node {i.index}: in_edges={len(i.in_edges())}, out_edges={len(i.out_edges())}")
    if len(i.in_edges()) == 0 and len(i.out_edges()) > 0:
        sources.append(i)
        # print(f"Node {i.index} initiates message (source node)")
# sources = [i for i in g.vs if g.vs[i].in_edges() == 0 and g.vs[i].out_edges() != 0]
for s in sources:
    q.append(s)
    print(f"Node {s.index} initiates message (source node)")

# Process nodes in topological order
while q:
    node = q.popleft()
    
    # Send message to all outgoing neighbors
    for neighbor in g.neighbors(node, mode="out"):
        print(f"Node {node.index} sends message to Node {neighbor}")
        received[neighbor] += 1
        total_messages += 1
        print(f"Node {neighbor} has received {received[neighbor]} messages")
        # If this neighbor has received messages from all incoming edges, enqueue it
        if received[neighbor] == g.vs[neighbor].in_edges():
            q.append(neighbor)

print(f"\nMessage passing simulation complete. Total messages sent: {total_messages}")

# After creating your graph g...

# Iterate through all nodes and get edge information
for v in g.vs:
    print(f"Node {v.index}:")
    
    # Outgoing edges (edges where this node is the source)
    out_edges = v.out_edges()
    print(f"  Outgoing edges: {len(out_edges)}")
    for e in out_edges:
        print(f"    -> Target: {e.target}, Edge index: {e.index}")
    
    # Incoming edges (edges where this node is the target)
    in_edges = v.in_edges()
    print(f"  Incoming edges: {len(in_edges)}")
    for e in in_edges:
        print(f"    <- Source: {e.source}, Edge index: {e.index}")
    
    print()  # Blank line for readability

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









#links
#https://python.igraph.org/en/main/index.html 