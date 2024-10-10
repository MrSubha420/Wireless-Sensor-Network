"""
Wireless Sensor Network Visualization and Communication Simulation

This program simulates a wireless sensor network using NetworkX and Dash.
It creates a network of nodes with random connections and visualizes the network using Plotly.
The program simulates communication steps between nodes, printing detailed information about
the sender, receiver, and the path taken for each communication step.

The stages of communication are:
1. Request: The sender node requests communication with the receiver node.
2. Acknowledgment: The receiver node acknowledges the communication request.
3. Data Transfer: Data is transferred from the sender node to the receiver node.

Each stage is visually represented in the network graph, and the program prints
the details of each stage to the console.
"""

import networkx as nx
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import random
import time
from datetime import datetime, timedelta

# Create a graph for the wireless sensor network
G = nx.Graph()

# Number of nodes
num_nodes = 8

# Add nodes to the graph
nodes = range(num_nodes)
G.add_nodes_from(nodes)

# Randomly add edges between nodes to simulate wireless connections
edges = [(i, j) for i in nodes for j in nodes if i < j and random.random() > 0.5]
G.add_edges_from(edges)

# Assign positions to nodes for visualization
pos = nx.spring_layout(G)

# Initialize Dash app
app = dash.Dash(__name__)

# State to track the transmission
transmission_state = {
    'step': 0,
    'paths': [],
    'start_time': None,
    'stage': 'idle'  # Track the current stage of communication
}

# Function to generate Plotly figure
def create_figure(paths, step, current_time):
    edge_trace = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace.append(go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None],
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines'))

    node_trace = go.Scatter(
        x=[], y=[],
        text=[],
        mode='markers+text',
        textposition='top center',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            )
        )
    )

    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        node_trace['text'] += tuple([str(node)])

    # Create a figure
    fig = go.Figure(data=edge_trace + [node_trace],
                    layout=go.Layout(
                        title=f'Wireless Sensor Network - Step {step}',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False)))

    # Add arrows for communication paths
    for path in paths:
        if isinstance(path, list):  # Ensure path is a list
            elapsed_time = (current_time - transmission_state['start_time']).total_seconds()
            if elapsed_time < 50:  # Show data transmission for 50 seconds
                for i in range(len(path) - 1):
                    x0, y0 = pos[path[i]]
                    x1, y1 = pos[path[i+1]]
                    fig.add_trace(go.Scatter(
                        x=[x0, x1],
                        y=[y0, y1],
                        mode='markers+lines+text',
                        marker=dict(size=10, color='red'),
                        line=dict(width=2, color='red'),
                        text=[f'{path[i]} -> {path[i+1]}'],
                        textposition='top center'
                    ))

    return fig

# App layout
app.layout = html.Div([
    dcc.Graph(id='network-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # Update every second
        n_intervals=0
    )
])

@app.callback(
    Output('network-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    global transmission_state
    step = transmission_state['step']
    current_time = datetime.now()

    # Only simulate communication steps up to 3 times
    if step < 6:
        if transmission_state['start_time'] is None or (current_time - transmission_state['start_time']).total_seconds() >= 50:
            source, target = random.sample(nodes, 2)
            path = simulate_communication(G, source, target)
            if path:
                transmission_state['paths'] = [path]  # Ensure paths is a list of paths
                transmission_state['start_time'] = current_time
                transmission_state['step'] += 1
                transmission_state['stage'] = 'request'
    
    # Print messages based on current stage
    if transmission_state['stage'] == 'request':
        path = transmission_state['paths'][0]
        path_str = ' -> '.join(map(str, path))
        print(f"Sender Node {path[0]} is requesting communication with Receiver Node {path[-1]} via path: {path_str}")
        transmission_state['stage'] = 'acknowledgment'
    elif transmission_state['stage'] == 'acknowledgment':
        elapsed_time = (current_time - transmission_state['start_time']).total_seconds()
        if elapsed_time >= 10:  # Wait for 10 seconds to simulate acknowledgment
            path = transmission_state['paths'][0]
            path_str = ' -> '.join(map(str, path))
            print(f"Receiver Node {path[-1]} has granted acknowledgment to Sender Node {path[0]} via path: {path_str}")
            transmission_state['stage'] = 'data_transfer'
    elif transmission_state['stage'] == 'data_transfer':
        elapsed_time = (current_time - transmission_state['start_time']).total_seconds()
        if elapsed_time >= 20:  # Wait for 20 seconds to simulate data transfer
            path = transmission_state['paths'][0]
            path_str = ' -> '.join(map(str, path))
            print(f"Data transfer from Sender Node {path[0]} to Receiver Node {path[-1]} via path: {path_str}")
            print("      ")
            transmission_state['stage'] = 'idle'
    
    return create_figure(transmission_state['paths'], step, current_time)

# Function to simulate communication steps
def simulate_communication(G, source, target):
    if nx.has_path(G, source, target):
        path = nx.shortest_path(G, source, target)
        return path
    else:
        print(f"No path found from Node {source} to Node {target}")
        return []

if __name__ == '__main__':
    app.run_server(debug=True)
