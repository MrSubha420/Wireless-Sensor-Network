import networkx as nx
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import random
from datetime import datetime
import threading
from collections import deque

# Create a graph for the wireless sensor network
G = nx.Graph()
num_nodes = 8
nodes = range(num_nodes)
G.add_nodes_from(nodes)
edges = [(i, j) for i in nodes for j in nodes if i < j and random.random() > 0.5]
G.add_edges_from(edges)
pos = nx.spring_layout(G)

# Initialize Dash app
app = dash.Dash(__name__)

# State to track the transmission
transmission_state = {
    'step': 0,
    'paths': [],
    'start_time': None,
    'stage': 'idle',
    'medium_free': True,
    'waiting_nodes': deque(),
    'collision': False,
    'backoff_time': 0,
    'active_path': None
}

# Dictionary to track the busy state of each path
path_busy = {}

# Lock for simulating medium access control
transmission_lock = threading.Lock()

# Function to generate Plotly figure
def create_figure(paths, step, current_time, waiting_nodes, collision):
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
        x=[],
        y=[],
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
            ),
            color=[]
        )
    )

    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'] += (x,)
        node_trace['y'] += (y,)
        if node in waiting_nodes:
            node_trace['text'] += (f'{node} (waiting)',)
            node_trace['marker']['color'] += ('orange',)
        else:
            node_trace['text'] += (str(node),)
            node_trace['marker']['color'] += ('blue',)

    path_trace = []
    for path in paths:
        if isinstance(path, list):
            elapsed_time = (current_time - transmission_state['start_time']).total_seconds()
            if elapsed_time < 50:  # Show data transmission for 50 seconds
                for i in range(len(path) - 1):
                    x0, y0 = pos[path[i]]
                    x1, y1 = pos[path[i+1]]
                    color = 'red' if collision else 'green'
                    path_trace.append(go.Scatter(
                        x=[x0, x1],
                        y=[y0, y1],
                        mode='markers+lines+text',
                        marker=dict(size=10, color=color),
                        line=dict(width=2, color=color),
                        text=[f'{path[i]} -> {path[i+1]}'],
                        textposition='top center'
                    ))

    fig = go.Figure(data=edge_trace + [node_trace] + path_trace,
                    layout=go.Layout(
                        title=f'Wireless Sensor Network - Step {step}',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False)))

    return fig

# App layout
app.layout = html.Div([
    dcc.Graph(id='network-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1*10000,  # Update every second
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

    # Handle backoff state
    if transmission_state['stage'] == 'backoff':
        elapsed_time = (current_time - transmission_state['start_time']).total_seconds()
        if elapsed_time >= transmission_state['backoff_time']:
            print(f"Backoff time completed. Node {transmission_state['waiting_nodes'][0]} retrying transmission.")
            transmission_state['collision'] = False
            transmission_state['stage'] = 'carrier_sensing'
        return create_figure(transmission_state['paths'], step, current_time, transmission_state['waiting_nodes'], transmission_state['collision'])

    # Only simulate communication steps up to 6 times
    if step < 6:
        if transmission_state['start_time'] is None or (current_time - transmission_state['start_time']).total_seconds() >= 50:
            if not transmission_state['waiting_nodes']:
                # Add new nodes to the waiting list if it's empty
                available_nodes = list(set(G.nodes()) - set(transmission_state['waiting_nodes']))
                if available_nodes:
                    source = random.choice(available_nodes)
                    target = random.choice(list(set(G.nodes()) - {source}))
                    path = simulate_communication(G, source, target)
                    if path:
                        transmission_state['paths'] = [path]
                        transmission_state['start_time'] = current_time
                        transmission_state['step'] += 1
                        transmission_state['stage'] = 'carrier_sensing'
                        transmission_state['waiting_nodes'].append(source)
                else:
                    print("No available nodes to send data. Waiting...")
            else:
                print(f"Node {transmission_state['waiting_nodes'][0]} waiting to transmit.")

    # CSMA/CD protocol stages
    if transmission_state['stage'] == 'carrier_sensing':
        path = transmission_state['paths'][0]
        path_key = tuple(path)
        if path_key not in path_busy or not path_busy[path_key]:
            path_busy[path_key] = True
            print(f"Node {path[0]} detected that the channel is clear. Proceeding to request.")
            transmission_state['stage'] = 'request'
        else:
            print(f"Collision detected on path {path}. Node {path[0]} will backoff.")
            transmission_state['collision'] = True
            transmission_state['backoff_time'] = random.randint(1, 10)
            transmission_state['stage'] = 'backoff'

    elif transmission_state['stage'] == 'request':
        path = transmission_state['paths'][0]
        with transmission_lock:
            path_key = tuple(path)
            if not path_busy[path_key]:
                path_busy[path_key] = True
                path_str = ' -> '.join(map(str, path))
                print(f"Node {path[0]} is requesting communication with Node {path[-1]} via path: {path_str}")
                transmission_state['stage'] = 'acknowledgment'
            else:
                print(f"Collision detected on path {path}.")
                transmission_state['collision'] = True
                transmission_state['backoff_time'] = random.randint(1, 10)
                transmission_state['stage'] = 'backoff'

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
            print("Data transfer successful.")
            print("Releasing nodes and medium.")
            path_key = tuple(path)
            path_busy[path_key] = False
            transmission_state['waiting_nodes'].popleft()
            transmission_state['stage'] = 'idle'
            transmission_state['collision'] = False

    return create_figure(transmission_state['paths'], step, current_time, transmission_state['waiting_nodes'], transmission_state['collision'])

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
