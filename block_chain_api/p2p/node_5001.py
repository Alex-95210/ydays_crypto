# import the GossipNode class
from gossipNode import GossipNode

# port for this node
port = 5001
# ports for the nodes connected to this node
connected_nodes = [5000]

node = GossipNode(port, connected_nodes)