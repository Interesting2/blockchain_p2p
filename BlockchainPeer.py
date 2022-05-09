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
        self.neighbour = [] # store a tuple | (id, port_no)

    def parse_file(self):
        with open(self.config_file, 'r') as f:
            lines = f.readlines()
            num_lines = lines[0].strip('\n')
            for i in range(1, num_lines + 1):
                neighbour_id, neigbour_port = lines[i].strip('\n').split(" ")
                neighbour_content = (neighbour_id, neigbour_port)
                self.neighbour.append(neighbour_content)
            print("Neighbours: ")
            print(self.neighbour)




    def run(self):
        file_content = self.parse_file()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 BlockchainPeer.py <Peer-Id> <PORT_NO> <Peer-Config-File>")
        exit(1)
    peer_id = sys.argv[1]
    port_no = sys.argv[2]
    config_file = sys.argv[3]
    blockchainPeer = BlockchainPeer(peer_id, port_no, config_file)
    blockchainPeer.run()
