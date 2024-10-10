import networkx as nx
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import random
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

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
    'current_slot': 0,
    'slot_duration': 50,  # Duration of each TDMA slot in seconds
    'frequency_bands': ['2.4GHz', '2.5GHz'],
    'last_update': datetime.now()
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
        if isinstance(path, list):
            elapsed_time = (current_time - transmission_state['start_time']).total_seconds()
            if elapsed_time < 50:
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

    # Update the current time
    current_time = datetime.now()
    
    # Check if it's time to switch TDMA slot
    if transmission_state['start_time'] is None:
        transmission_state['start_time'] = current_time

    elapsed_time = (current_time - transmission_state['start_time']).total_seconds()
    if elapsed_time >= transmission_state['slot_duration']:
        transmission_state['step'] += 1
        transmission_state['start_time'] = current_time
        transmission_state['current_slot'] += 1
        if transmission_state['step'] % 2 == 0:
            # Simulate TDMA communication
            source, target = random.sample(nodes, 2)
            path = simulate_tdma_communication(G, source, target)
        else:
            # Simulate FDMA communication
            source, target = random.sample(nodes, 2)
            path = simulate_fdma_communication(G, source, target)
        
        if path:
            transmission_state['paths'] = [path]
            fdma_band = transmission_state['frequency_bands'][transmission_state['current_slot'] % len(transmission_state['frequency_bands'])]
            if transmission_state['step'] % 2 == 0:
                # Print TDMA communication details
                print(f"TDMA: Communication between Node {path[0]} and Node {path[-1]} using path: {' -> '.join(map(str, path))}")
                print(f"TDMA Slot: {transmission_state['current_slot']}")
                print(f"Sender Node {path[0]} is requesting communication with Receiver Node {path[-1]} via path: {' -> '.join(map(str, path))}")
            else:
                # Print FDMA communication details
                print(f"FDMA: Communication between Node {path[0]} and Node {path[-1]} using path: {' -> '.join(map(str, path))}")
                print(f"FDMA Frequency Band: {fdma_band}")
                print(f"Sender Node {path[0]} is requesting communication with Receiver Node {path[-1]} via path: {' -> '.join(map(str, path))}")

    return create_figure(transmission_state['paths'], transmission_state['step'], current_time)

# Function to simulate TDMA communication steps
def simulate_tdma_communication(G, source, target):
    if nx.has_path(G, source, target):
        path = nx.shortest_path(G, source, target)
        return path
    else:
        print(f"No path found from Node {source} to Node {target}")
        return []

# Function to simulate FDMA communication steps
def simulate_fdma_communication(G, source, target):
    if nx.has_path(G, source, target):
        path = nx.shortest_path(G, source, target)
        return path
    else:
        print(f"No path found from Node {source} to Node {target}")
        return []

if __name__ == '__main__':
    app.run_server(debug=True)
