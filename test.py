import requests
from blockchain import BlockChain, Block

blockchain = BlockChain()
#block1 = Block(self.index, self.proof, self.previous_hash, self.transactions)

def print_blockchain(chain):
    for block in chain:
        print(vars(block))


def class_tests():
    print("Length of Current blockchain is: {}".format(len(blockchain.chain)))
    print_blockchain(blockchain.chain)
    #print("The hash of the block is: " block1.get_block_hash)
    blockchain.mine_block('address_x')
    print("\nAfter Mining 1st Block")
    print("Length of Updated blockchain is: {}".format(len(blockchain.chain)))
    print_blockchain(blockchain.chain)
    blockchain.mine_block('address_y')
    print("\nAfter Mining 2nd Block")
    print("Length of Updated blockchain is: {}".format(len(blockchain.chain)))
    print_blockchain(blockchain.chain)


def register_node(node_addr, parent_server):
    resp = requests.post(parent_server + '/register-node', json={'address': node_addr})
    print("\nOn Server {}: Node-{} has been registered successfully!\n".format(parent_server, node_addr))
    return resp


def create_transaction(server, data):
    resp = requests.post(server + '/create-transaction', json=data).json()
    print("On Server {}: Transaction has been processed!\n".format(server))
    return resp


def mine_block(server):
    resp = requests.get(server + '/mine').json()
    print("On Server {}: Block has been mined successfully!\n".format(server))
    return resp


def get_server_chain(server):
    resp = requests.get(server + '/chain').json()
    print("On Server {}: Chain is-\n{}\n".format(server, resp))
    return resp


def sync_chain(server_1, server_2):
    print("On Server {}: Started Syncing Chain from the host Server {}".format(server_1,server_2))
    resp = requests.get(server_1 + '/sync-chain')
    print("On Server {}: Chain synced!\n".format(server_1))
    return resp


def api_tests():
    server1 = 'http://127.0.0.1:5000'
    server2 = 'http://127.0.0.1:5001'
    server3 = 'http://127.0.0.1:5002'
    register_node(server2, server1)  # server2 node will be register inside server1    
    create_transaction(server2, {"sender": "Vishnu", "recipient": "Harsha", "amount": 10000})
    mine_block(server2)  # Mined a new block on server2
    create_transaction(server2, {"sender": "Charan", "recipient": "Vishnu", "amount": 20000})
    mine_block(server2)
    register_node(server3, server1)  # server2 node will be register inside server1
    register_node(server3, server2)
    get_server_chain(server1)  # server1's chain
    get_server_chain(server2)  # server2's chain
    get_server_chain(server3)
    sync_chain(server3,server2)  # updating server1's chain with neighbouring node's chain
    sync_chain(server1,server2)
    sync_chain(server3,server1)
    get_server_chain(server1)  # server1's chain after syncing
    get_server_chain(server2)
    get_server_chain(server3)
    #create_transaction(server1, {"sender": "Ram", "recipient": "Harsha", "amount": 15000})
    #mine_block(server1)
    #get_server_chain(server1)
    #sync_chain(server2,server1)
    #get_server_chain(server2)

if __name__ == "__main__":
    #class_tests()
    api_tests()