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

def get_connected_nodes(actualPort):
    port=5000
    max_port=6000
    sock = socket.socket(type=socket.SOCK_DGRAM)
    connectedports= []
    while port <= max_port:
        try:
            sock.bind(("127.0.0.1", port))
            sock.close()
            print(port)
            if (port != actualPort):
                connectedports.append(port)
        except OSError:
            port += 1
    return connectedports

port = next_free_port()
connectedNodes= get_connected_nodes(actualPort=port)
node = GossipNode(port, [5000,5001,5002])