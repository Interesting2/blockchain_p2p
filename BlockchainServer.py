from _thread import *
import threading
import time
import datetime
import socket
import _thread
import json 
import hashlib
from Blockchain import Blockchain
from Transaction import Transaction

IP = "127.0.0.1"

# this variable can be used in case of avoiding deadlock
counter = 0
cc = ""

class BlockchainServer():
    def __init__(self, *args):
        self.peer_id, self.port_no, self.neighbours = args
        self.proof = 100
        self.blockchain = Blockchain()
        self.saved_address = {}

    def validate_pow(self, blockchain):

        proof = int(blockchain[-1]['proof'])
        prev_proof = int(blockchain[-2]['proof'])
        hash_operation = hashlib.sha256(str(proof**2 - prev_proof**2).encode('utf-8')).hexdigest()

        # validate first two digit of the hash
        return hash_operation[:2] == '00'


    def sync_blockchain(self, blockchain):
        # compare own blockchain with blockchain received from other servers

        # if the length of other peer's blockchain is greater than own blockchain, then update own blockchain
        if len(blockchain) > len(self.blockchain.blockchain):
            # validate pow based on the last two blocks
            if self.validate_pow(blockchain):

                self.blockchain.blockchain = blockchain
                # discard transactions that are part of the last block
                # especially when peer joined late and received lesser transactions 
                last_block = blockchain[-1]
                transactions = last_block['transaction']

                for transaction in transactions:
                    if transaction in self.blockchain.pool:
                        self.blockchain.pool.remove(transaction)
            else:
                return


    def periodic_heartbeat(self):
        while True:
            if cc == 'cc':
                return
            requestContent = "hb"
            mess_data = bytes(requestContent, encoding= 'utf-8')

            # sending hb request to other peers
            for neighbour in self.neighbours:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((IP, self.neighbours[neighbour]))
                        s.sendall(mess_data)

                        data_rev = s.recv(1024) # blockchain received in json from all other servers
                        blockchainJson = data_rev.decode('utf-8')

                        # compare own blockchain with blockchain received from other servers
                        blockchain = json.loads(blockchainJson)
                        self.sync_blockchain(blockchain)

                        s.close()
                except Exception as e:
                    pass

            time.sleep(5)

    def serverHandler(self, c , addr, sock):

        while(True):
            global counter
            global cc
            counter += 1 

            # Parsing and processing data from client
            try:
                data_rev = c.recv(1024)
                if len(data_rev) == 0 or not data_rev:
                    break

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


                        # broadcast transaction to other peers
                        if c in self.saved_address:

                            # deal with problems where transaction can't be broadcasted to some peers
                            for neighbour in self.neighbours:
                                try:
                                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                                        s.connect((IP, self.neighbours[neighbour]))
                                        s.sendall(bytes(dataString, encoding= 'utf-8'))

                                        data_rev = s.recv(1024)
                                        response = data_rev.decode('utf-8')
                                        s.close()
                                except Exception as e:
                                    pass
                    else:
                        clientData = "Rejected"

                # Handle pb request
                elif typeRequest == 'pb':
                    clientData = json.dumps(self.blockchain.blockchain, indent=2, sort_keys=False)

                # Handle cc request
                elif typeRequest == 'cc':
                    cc = 'cc'
                    clientData = "Connection closed!"

                # Handle gp request
                elif typeRequest == 'gp':
                    # get current proof of work of the lastest block
                    clientData = str(self.blockchain.lastBlock()['proof'])

                
                # Handle up request
                elif typeRequest == 'up':
                    dataContent = dataString.split("|")
                    if len(dataContent) == 2:
                        proof = int(dataContent[1])

                        # checks correctness of proof
                        prev_proof = self.blockchain.lastBlock()['proof']
                        hash_operation = hashlib.sha256(str(proof**2 - prev_proof**2).encode('utf-8')).hexdigest()
                        if hash_operation[:2] == '00':
                            self.proof = proof
                            clientData = "Reward"
                        else:
                            clientData = "No Reward"
                    else:
                        clientData = "No Reward"

                # Handle hb request 
                elif typeRequest == 'hb':
                    # returns current blockchain in json
                    clientData = json.dumps(self.blockchain.blockchain, indent=1, sort_keys=False)
                    

                # Handle unknown request
                else:
                    clientData = "Unknown request"

                # create new block if #transactions == 5
                if len(self.blockchain.pool) == 5:
                    self.blockchain.newBlock(self.proof)

                clientData = bytes(clientData, encoding='utf-8')
                c.sendall(clientData)
                
                if typeRequest == 'cc':
                    break
            except Exception as e:
                break
        c.close()
        if cc == 'cc':
            sock.close()
        return

    def run(self):
        global counter
        global cc

        # periodic hb request thread
        threading.Thread(target=self.periodic_heartbeat, args=()).start()

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

                s.bind((IP, self.port_no)) # Bind to the port
                s.listen(5)
                while True:
                    # to avoid deadlock, counter can be used here: if counter == 6 or cc = 'cc':
                    if cc == 'cc' or counter == 6: 
                        break
                    c, addr = s.accept()
                    if c not in self.saved_address and len(self.saved_address) < 2:
                        self.saved_address[c] = addr

                    threading.Thread(target=self.serverHandler, args=(c, addr, s)).start()
                s.close()
                
        except Exception as e:
            print("Server Socket issue or Server Socket closed")
        
        return