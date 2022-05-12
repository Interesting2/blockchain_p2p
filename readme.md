**How to Start Program and Running Environment**

    ***Install and setup python3***
    Do python3 --version to check if it is installed correctly
    If not, follow the instructions in this page: https://realpython.com/installing-python/

    Create 3 terminals
    Run the following 3 commands in 3 different terminals/shells (1 command in each terminal)
    Note: Remember not to run the same command twice or more in different terminals

    python3 BlockchainPeer.py 1 6000 config_A.txt
    python3 BlockchainPeer.py 2 6001 config_B.txt
    python3 BlockchainPeer.py 3 6002 config_C.txt

    After running each command, you will see "Please enter your command: " is displayed in the terminal.
    You have 3 supported request options to type.
        tx request format: tx sender content 
        pb request format: pb 
        cc request format: cc 

        tx request allows you to send a transaction
        pb request allows you to print the current blockchain state
        cc request allows you to quit receiving and sending requests


    One thing you can test is to quit the program in one of your terminal by doing ctrl-c, close the terminal and reopen it.
    Run the same command that you did before in that terminal to let that peer node join the network again and be active.
