import random

class Node:
    def __init__(self, node_id, position, role='sensor'):
        self.node_id = node_id
        self.position = position
        self.role = role
        self.energy = 100  # Assume all nodes start with 100 units of energy
        self.data_queue = []

    def queue_data(self, data):
        self.data_queue.append(data)

    def process_data_queue(self, network):
        while self.data_queue:
            data = self.data_queue.pop(0)
            if data['destination'] == self:
                print(f"Node {self.node_id} received data: {data['content']}")
            else:
                recipient = self.find_next_hop_aodv(network, data['destination'])
                if recipient:
                    print(f"Node {self.node_id} forwarding data to Node {recipient.node_id}")
                    self.send_data(recipient, data)

    def find_next_hop_aodv(self, network, destination):
        # Simplified routing: forward to a random neighbor (for demo purposes)
        neighbors = network.get_neighbors(self)
        if not neighbors:
            return None
        return random.choice(neighbors)

    def send_data(self, recipient, data):
        recipient.queue_data(data)

    def send_rreq(self, network, destination):
        print(f"Node {self.node_id} broadcasting RREQ for Node {destination.node_id}")
        rreq = {'source': self, 'destination': destination}
        for neighbor in network.get_neighbors(self):
            network.send_rreq(neighbor, rreq)

    def receive_rreq(self, network, rreq):
        if rreq['destination'] == self:
            print(f"Node {self.node_id} received RREQ from Node {rreq['source'].node_id}")
            rrep = {'source': self, 'destination': rreq['source']}
            network.send_rrep(rreq['source'], rrep)
        else:
            self.send_rreq(network, rreq['destination'])

    def receive_rrep(self, network, rrep):
        print(f"Node {self.node_id} received RREP from Node {rrep['source'].node_id}")

    def send_route_request(self, network, route_request):
        print(f"Node {self.node_id} broadcasting route request")
        for neighbor in network.get_neighbors(self):
            network.send_route_request(neighbor, route_request)

    def receive_route_request(self, network, route_request):
        print(f"Node {self.node_id} received route request from Node {route_request['source'].node_id}")

    def receive_route_reply(self, network, route_reply):
        print(f"Node {self.node_id} received route reply from Node {route_reply['source'].node_id}")
