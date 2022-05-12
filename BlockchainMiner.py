from _thread import *
import threading
import time
import socket
import _thread
import sys
import json
import hashlib
import time

HOST = "127.0.0.1"

class BlockchainMiner():
    def __init__(self, *args):
        self.peer_id, self.port_no, self.neighbours = args
        self.latest_proof = 0
    
    def run(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, self.port_no))
                
                while True:
                    latest_proof = self.get_proof(s)

                    if latest_proof != self.latest_proof:

                        self.latest_proof = latest_proof
                        new_proof = self.proof_of_work(latest_proof)
                        self.update_proof(new_proof, s)
                    time.sleep(1)
                s.close()
        except Exception as e:
            print(e)
            print("Miner Can't connect to the Socket")
    
    def get_proof(self, s):
        # send request to server
        requestString = "gp"
        data = None
        s.send(requestString.encode('utf-8'))
        data = s.recv(1024)
       
        return int(data.decode('utf-8'))


    def update_proof(self, new_proof, s):
        requestString = "up | " + str(new_proof)
        # send request to server
        s.send(requestString.encode('utf-8'))
        data = s.recv(1024)     # receive reward or no reward from server
        print(data.decode('utf-8'))

    def calculateHash(self, data):
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def proof_of_work(self, prev_proof):
        new_proof = 0
        data = str(new_proof ** 2 - prev_proof ** 2)
        while self.calculateHash(data)[:2] != '00':
            new_proof += 1
            data = str(new_proof ** 2 - prev_proof ** 2)
        return new_proof

