# import the GossipNode class
from gossipNode import GossipNode
import socket

def next_free_port( port=5000, max_port=6000 ):
    sock = socket.socket(type=socket.SOCK_DGRAM)
    while port <= max_port:
        try:
            sock.bind(("127.0.0.1", port))
            sock.close()
            return port
        except OSError:
            port += 1
    raise IOError('no free ports')

port = next_free_port()
node = GossipNode(port, [port+1])