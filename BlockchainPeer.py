from ast import parse
from Blockchain import Blockchain
from Transaction import Transaction
from BlockchainServer import BlockchainServer
from BlockchainClient import BlockchainClient
from BlockchainMiner import BlockchainMiner
import sys

class BlockchainPeer():
    def __init__(self, *args):
        self.peer_id, self.port_no, self.config_file = args
        self.neighbour = {} # store id as key, port_no as value

    def setUpNeighbours(self):
        with open(self.config_file, 'r') as f:
            lines = f.readlines()
            num_lines = int(lines[0].strip('\n'))
            for i in range(1, num_lines + 1):
                neighbour_id, neigbour_port = lines[i].strip('\n').split(" ")
                self.neighbour[neighbour_id] = neigbour_port
            print("Neighbours: ")
            print(self.neighbour)




    def run(self):
        self.setUpNeighbours()

        # create miner, server and client
        server = BlockchainServer(self.peer_id, self.port_no, self.neighbour)
        client = BlockchainClient(self.peer_id, self.port_no, self.neighbour)
        miner = BlockchainMiner(self.peer_id, self.port_no, self.neighbour)

        # start server, client and miner
        server.run()
        client.run()
        miner.run()



if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 BlockchainPeer.py <Peer-Id> <PORT_NO> <Peer-Config-File>")
        exit(1)
    peer_id = sys.argv[1]
    port_no = sys.argv[2]
    config_file = sys.argv[3]
    blockchainPeer = BlockchainPeer(peer_id, port_no, config_file)
    blockchainPeer.run()
