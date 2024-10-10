import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# Define constants
NB_NODES = 20  # Total number of nodes
NB_CLUSTERS = 5  # Number of clusters
SIMULATION_ROUNDS = 6  # Number of rounds
DATA_AGGREGATION_COST = 0.1  # Cost of data aggregation (arbitrary units)
SLEEP_MODE_COST = 0.05  # Cost of being in sleep mode (arbitrary units)
ACTIVE_MODE_COST = 0.2  # Cost of being in active mode (arbitrary units)

class Node:
    def __init__(self, node_id, x, y):
        self.node_id = node_id
        self.x = x
        self.y = y
        self.is_cluster_head = False
        self.next_hop = None
        self.energy = 1.0  # Initial energy
        self.state = 'ACTIVE'  # Can be 'ACTIVE' or 'SLEEP'

    def distance_to(self, other_node):
        return np.sqrt((self.x - other_node.x) ** 2 + (self.y - other_node.y) ** 2)

    def consume_energy(self, mode):
        if mode == 'ACTIVE':
            self.energy -= ACTIVE_MODE_COST
        elif mode == 'SLEEP':
            self.energy -= SLEEP_MODE_COST

    def __str__(self):
        return f"Node {self.node_id}, Energy: {self.energy:.2f}, State: {self.state}"

class Network:
    def __init__(self):
        self.nodes = []
        self.create_nodes()

    def create_nodes(self):
        for i in range(NB_NODES):
            x = np.random.uniform(0, 100)
            y = np.random.uniform(0, 100)
            self.nodes.append(Node(i, x, y))

    def get_alive_nodes(self):
        return [node for node in self.nodes if node.energy > 0]

    def broadcast_next_hop(self):
        for node in self.nodes:
            print(f'Node {node.node_id} -> Next Hop: {node.next_hop}')
            print(node)

def data_aggregation_cost(node):
    return DATA_AGGREGATION_COST if node.is_cluster_head else 0

def leach_setup_phase(network):
    prob_ch = NB_CLUSTERS / NB_NODES
    heads = []
    alive_nodes = network.get_alive_nodes()

    # Decide which nodes are cluster heads
    idx = 0
    while len(heads) < NB_CLUSTERS:
        node = alive_nodes[idx]
        if np.random.uniform(0, 1) < prob_ch:
            node.is_cluster_head = True
            node.next_hop = 'BSID'  # Base Station ID
            heads.append(node)
        idx = (idx + 1) % len(alive_nodes)

    # Ordinary nodes choose nearest cluster heads
    for node in alive_nodes:
        if node.is_cluster_head:
            node.consume_energy('ACTIVE')  # CH is active
            node.state = 'ACTIVE'
        else:
            nearest_head = heads[0]
            for head in heads[1:]:
                if node.distance_to(head) < node.distance_to(nearest_head):
                    nearest_head = head
            node.next_hop = nearest_head.node_id
            node.consume_energy('SLEEP')  # Ordinary nodes sleep
            node.state = 'SLEEP'

    network.broadcast_next_hop()

def plot_network(nodes):
    G = nx.Graph()
    pos = {node.node_id: (node.x, node.y) for node in nodes}

    # Add nodes to the graph
    for node in nodes:
        G.add_node(node.node_id, pos=(node.x, node.y), color='blue' if node.is_cluster_head else 'red')

    # Add edges based on next_hop
    for node in nodes:
        if node.next_hop != 'BSID' and node.next_hop in G.nodes:
            G.add_edge(node.node_id, node.next_hop)

    # Draw the network
    colors = [G.nodes[n]['color'] for n in G.nodes]
    nx.draw(G, pos, node_color=colors, with_labels=True, node_size=100, edge_color='gray', font_size=8, font_color='black')

    plt.title('Network Nodes with LEACH Protocol')
    plt.show()

# Main execution
network = Network()
for _ in range(SIMULATION_ROUNDS):
    leach_setup_phase(network)
    plot_network(network.get_alive_nodes())
