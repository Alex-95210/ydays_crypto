import random
import socket
from threading import Thread
import time
from datetime import datetime


class GossipNode:
    # pass the port of the node and the ports of the nodes connected to it
    def __init__(self, port, connected_nodes):
        # create a new socket instance
        # use SOCK_DGRAM to be able to send data without a connection
        # being established (connectionless protocol)
        self.node = socket.socket(type=socket.SOCK_DGRAM)
        self.previous_message = ''

        # set the address, i.e(hostname and port) of the socket
        self.hostname = "127.0.0.1"
        self.port = port

        # bind the address to the socket created
        self.node.bind((self.hostname, self.port))

        # set the ports of the nodes connected to it as susceptible nodes
        self.susceptible_nodes = connected_nodes

        # call the threads to begin the magic
        self.start_threads()

    def input_message(self):
        while True:
            # input message to send to all nodes
            message_to_send = input("Enter a message to send: ")

            # call send message method and pass the input message.
            # encode the message into ascii
            self.transmit_message(message_to_send.encode('ascii'), 0)

    def receive_message(self):
        while True:

            # since we are using connectionless protocol,
            # we will use 'recvfrom' to receive UDP message
            
            message_to_forward, address = self.node.recvfrom(1024)
            

            if self.previous_message == message_to_forward:
                continue
            self.previous_message = message_to_forward


            previous_node = address[1]
            print('\nMessage to forward, address: {}, {}'.format(message_to_forward, address[1]))

            # sleep for 2 seconds in order to show difference in time
            time.sleep(1)

            # print message with the current time.
            # decode message so as to print it, as it was sent
            print("\nReceived message: '{0}'. From [{1}]"
                    .format(message_to_forward.decode('ascii'), address[1]))

            # call send message to forward the message to other susceptible(connected) nodes
            self.transmit_message(message_to_forward, previous_node)

    def transmit_message(self, message, previous_node=0):
        for i in range(len(self.susceptible_nodes)):
            selected_port = self.susceptible_nodes[i]

            if selected_port == previous_node:
                continue

            # since we are using connectionless protocol,
            # we will use 'sendto' to transmit the UDP message
            self.node.sendto(message, (self.hostname, selected_port))

            time.sleep(1)

    def start_threads(self):
        # two threads for entering and getting a message.
        # it will enable each node to be able to
        # enter a message and still be able to receive a message
        Thread(target=self.input_message).start()
        Thread(target=self.receive_message).start()