import json
import random
import socket
from threading import Thread
import time
import blockchain as blockchainClass


bc = blockchainClass.Blockchain()


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
            message_to_send = 0
            # input message to send to all nodes
            print(" ")
            print("1 - to see block chain")
            print("2 - to create a b2c transaction")
            print("3 - to create a c2c transaction")
            print("4 - to check first sell date of a helmet")
            print("5 - to check helmet authenticity")
            print("6 - to check chain authenticity")
            command = input('what do you want to do : ')
            print(" ")
            if command == "1":
                data = bc.get_db(self.port)
                print(data)
            if command == "2":
                serieNum = input("enter the serie number : ")
                model = input("enter the model : ")
                color = input("enter the color : ")
                token = bc.createToken(serieNum, model, color)
                brandHash = input("enter your hash : ")
                buyerHash = input("enter the buyer hash : ")
                print(" ")
                print("Your helmet token is "+ token)
                transaction = bc.createTransaction(token, brandHash, buyerHash)
                block = bc.mine(transaction, self.port)
                message_to_send = json.dumps(block)
            if command == "3":
                token = input("enter the token : ")
                brandHash = input("enter your hash : ")
                buyerHash = input("enter the buyer hash : ")
                transaction = bc.createTransaction(token, brandHash, buyerHash)
                block = bc.mine(transaction, self.port)
                message_to_send = json.dumps(block)
            if command == "4":
                token = input("enter the token : ")
                helmet_age = bc.get_helmet_age(token, self.port)
                print("The helmet is "+helmet_age+" years old.")
            if command == "5":
                serieNum = input("enter the serie number : ")
                model = input("enter the model name : ")
                color = input("enter the color : ")
                isValid = bc.checkHelmetAuthenticity(serieNum, model, color, self.port)
                if isValid:
                    print("the helmet is a "+str(isValid)+" one")
                else:
                    print("the helmet is a "+str(isValid)+" one, you got fooled dude...")
            if command == "6":
                chain = bc.get_db(self.port)
                isValid = bc.is_chain_valid(chain)
                if isValid:
                    print("the chain is valid")
                else:
                    print("the chain is invalid")
            if command == "7":
                token = input("enter the token : ")
                ownerHash = bc.findOwner(token, self.port)
                print("the owner hash is "+ownerHash)
            # call send message method and pass the input message.
            # encode the message into ascii
            if message_to_send != 0:
                self.transmit_message(message_to_send.encode('utf-8'), 0)

    def receive_message(self):
        while True:

            # since we are using connectionless protocol,
            # we will use 'recvfrom' to receive UDP message
            
            message_to_forward, address = self.node.recvfrom(1024)
            

            if self.previous_message == message_to_forward:
                continue
            self.previous_message = message_to_forward


            previous_node = address[1]

            dataReceived = message_to_forward.decode('utf-8')
            dataJson = json.loads(dataReceived)
            bc.add_to_db(dataJson, self.port, dataJson["index"])
            chain = bc.get_db(self.port)
            isValid = bc.is_chain_valid(chain)
            if isValid:
                self.transmit_message(message_to_forward, previous_node)
            else:
                bc.remove_last_block(dataJson["index"], self.port)
            
    def transmit_message(self, message, previous_node):
        for i in range(len(self.susceptible_nodes)):
            selected_port = self.susceptible_nodes[i]

            if selected_port == self.port:
                continue
            if selected_port == previous_node:
                continue
            # since we are using connectionless protocol,
            # we will use 'sendto' to transmit the UDP message
            self.node.sendto(message, (self.hostname, selected_port))


    def start_threads(self):
        # two threads for entering and getting a message.
        # it will enable each node to be able to
        # enter a message and still be able to receive a message
        Thread(target=self.input_message).start()
        Thread(target=self.receive_message).start()