# import the GossipNode class
from gossipNode import GossipNode

# port for this node
port = 5003
# ports for the nodes connected to this node
connected_nodes = [5002]

node = GossipNode(port, connected_nodes)