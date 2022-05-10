from _thread import *
import threading
import time
import datetime
import socket
import _thread
import json 
from Blockchain import Blockchain
from Transaction import Transaction

IP = "127.0.0.1"
# PORT_Server = 1993

# this variable can be used in case of avoiding deadlock
counter = 0
cc = ""

class BlockchainServer():
    def __init__(self, *args):
        self.peer_id, self.port_no, self.neighbours = args
        self.proof = 100
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
                print(json.dumps(self.blockchain.blockchain, indent=2, sort_keys=False))
                clientData = str(self.blockchain.blockchain)

            # Handle cc request
            elif typeRequest == 'cc':
                cc = 'cc'
                clientData = "Connection closed!"

            # Handle gp request
            elif typeRequest == 'gp':
                # get current proof of work of the lastest block
                # currentProof = self.blockchain.getLastBlock().proof
                clientData = self.blockchain.getLastBlock().proof

            
            # Handle up request
            elif typeRequest == 'up':
                # update proof of work of the lastest block
                dataContent = dataString.split("|")
                if len(dataContent) == 2:
                    proof = dataContent[1]
                    self.proof = proof
                    clientData = "Updated Proof in Server"
                else:
                    clientData = "Proof not updated in Server"

            # Handle hb request 
            elif typeRequest == 'hb':
                # returns current blockchain in json
                clientData = json.dumps(self.blockchain.blockchain, indent=1, sort_keys=False)
                

            # Handle unknown request
            else:
                clientData = "Unknown request"


            # create new block if #transactions == 5
            if len(self.blockchain.pool) == 5:
                # calc proof of work
                self.blockchain.newBlock(proof)

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
                print("Blockchain Server host names: ", IP, "Port: ", self.port_no)
                s.bind((IP, self.port_no)) # Bind to the port
                s.listen(5)
                while True:
                    # to avoid deadlock, counter can be used here: if counter == 6 or cc = 'cc':
                    if cc == 'cc' or counter == 6: 
                        break
                    c, addr = s.accept()
                    _thread.start_new_thread(self.serverHandler,(c, addr))
                s.close()
                return
        except:
            print("Can't connect to the Socket")

# server = BlockchainServer()
# server.run()