from _thread import *
import threading
import time
import socket
import _thread
import sys
import json

HOST = "127.0.0.1"
# PORT_Server = 1993

class BlockchainClient():
    def __init__(self, *args):
        self.peer_id, self.port_no, self.neighbours = args
        self.args = args    

    

    def run(self):
        # _thread.start_new_thread(self.periodic_heartbeat, ())   # new thread for sending hb requests
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # Create a socket object
                s.connect((HOST, self.port_no))
                # print("From client (peername): ", s.getpeername())
                # print("From client (sockname): ", s.getsockname())

                while(1):
            
                    # Parser for input command
                    commandContent = input("Please enter your command: ")
                    print("CLIENT ASKING")
                    content = commandContent.split(" ")
                    commandType = content[0]

                    # Process command
                    if commandType == 'tx':
                        if len(content) != 3:
                            print("Invalid transaction!")
                            continue
                        else:
                            requestContent = f"tx|{str(content[1])}|{str(content[2])}"
                            print(requestContent)
                    elif commandType == 'pb':
                        if len(content) != 1:
                            print("Invalid arguments for pb request!")
                            continue
                        else:
                            requestContent = "pb"
                    elif commandType == 'cc':
                        if len(content) != 1:
                            print("Invalid arguments for cc request!")
                            continue
                        else:
                            requestContent = "cc"
                    else:
                        print("Please enter the supported request: ")
                        print("tx sender content -- [tx: command type of transaction] [sender of transaction] [content of transaction]")
                        print("pb -- [pb: command type of Print Blockchain]")
                        print("cc -- [cc: command type of Close Connection]")
                        continue    
                    
                    # Create message for sending to Blockchain server
                    mess_data = bytes(requestContent, encoding= 'utf-8')
                    s.sendall(mess_data)

                    # Parse response from blockchain server
                    data_rev = s.recv(1024)
                    dataString = data_rev.decode('utf-8')
                    if not data_rev:
                        print("didn't get data")
                        break
                    if commandType == 'pb':
                        # blockchainJson = json.loads(dataString)
                        print(json.dumps(dataString, indent=2, sort_keys=False))
                    elif commandType == 'cc':
                        print("Client: ", dataString)
                        break
                    elif commandType == 'tx':
                        print("Client Transaction response from server: ", dataString)
                    else:
                        print("Server general response to Client: ", dataString)
                s.close()   
        except Exception as e:

            print("Can't connect to the Blockchain server")
            print(e)
        print("END OF CLIENT")

# client = BlockchainClient('A', 6000, {})
# client.run()