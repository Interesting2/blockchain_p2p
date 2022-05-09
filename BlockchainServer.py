from _thread import *
import threading
import time
import datetime
import socket
import _thread
import json 
from Blockchain import Blockchain
from Transaction import Transaction
IP = "127.0.0.1" # '' -> localhost
PORT_Server = 1993

# this variable can be used in case of avoiding deadlock
counter = 0
cc = ""

class BlockchainServer():
    def __init__(self, *args):
        self.args = args
        self.blockchain = Blockchain()

    def serverHandler(self, c , addr):
        while(True):
            global counter
            global cc
            counter += 1 

            # Parsing and processing data from client
            data_rev = c.recv(1024)
            dataString = data_rev.decode('utf-8')
            typeRequest = dataString[:2]
            clientData = ""
            # Handle tx request
            if typeRequest == 'tx':
                transaction = Transaction()
                transactionContent = transaction.validateTransaction(dataString)
                if transactionContent != None:
                    self.blockchain.addTransaction(transactionContent)
                    clientData = "Accepted"
                else:
                    clientData = "Rejected"
            # Handle pb request
            elif typeRequest == 'pb':
                print(json.dumps(self.blockchain.blockchain, indent=1, sort_keys=False))
                clientData = str(self.blockchain.blockchain)

            # Handle cc request
            elif typeRequest == 'cc':
                cc = 'cc'
                clientData = "Connection closed!"
            
            # create new block if #transactions > 3
            if len(self.blockchain.pool) == 3:
                self.blockchain.newBlock(123)

            clientData = bytes(clientData, encoding='utf-8')
            c.sendall(clientData)
            
            if typeRequest == 'cc':
                break
        c.close()
        return

    def run(self):
        global counter
        global cc
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print("Blockchain Server start") 
                print("Blockchain Server host names: ", IP, "Port: ",PORT_Server)
                s.bind((IP, PORT_Server)) # Bind to the port
                s.listen(5)
                while True:
                    # to avoid deadlock, counter can be used here: if counter == 6 or cc = 'cc':
                    if cc == 'cc': 
                        break
                    c, addr = s.accept()
                    _thread.start_new_thread(self.serverHandler,(c, addr))
                s.close()
                return
        except:
            print("Can't connect to the Socket")

server = BlockchainServer()
server.run()