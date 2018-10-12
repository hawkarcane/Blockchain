from uuid import uuid4
import requests
from flask import Flask, jsonify, url_for, request
from blockchain import BlockChain, Block
from argparse import ArgumentParser

app = Flask(__name__)
blockchain = BlockChain()
#block1 = Block(self.index, self.proof, self.previous_hash, self.transactions)
node_address = uuid4().hex  # Unique address for current node


@app.route('/create-transaction', methods=['POST'])
def create_transaction():
    transaction_data = request.get_json()
    index = blockchain.create_new_transaction(**transaction_data)
    response = {
        'message': 'Transaction has been submitted successfully',
        'block_index': index
    }
    return jsonify(response)


@app.route('/mine', methods=['GET'])
def mine():
    block = blockchain.mine_block(node_address)
    response = {
        'message': 'Successfully Mined the new Block',
        'block_data': block
    }
    return jsonify(response)


@app.route('/chain', methods=['GET'])
def get_full_chain():
    response = {
        'chain': blockchain.get_serialized_chain
    }
    return jsonify(response)

'''
@app.route('/hash', methods=['GET'])
def get_current_hash():
    response = {
        'current hash': block1.get_block_hash
    }
    return jsonify(response)
'''

@app.route('/register-node', methods=['POST'])
def register_node():
    node_data = request.get_json()
    blockchain.create_node(node_data.get('address'))
    response = {
        'message': 'New node has been added',
        'node_count': len(blockchain.nodes),
        'nodes': list(blockchain.nodes),
    }
    return jsonify(response)
'''
def resolve_conflicts():

    neighbours = blockchain.nodes
    new_chain = None

    # We're only looking for chains longer than ours
    max_length = len(blockchain.chain)

    # Grab and verify the chains from all the nodes in our network
    for node in neighbours:
        print('http://' + node + '/chain')
        response = requests.get('http://' + node + '/chain')
        if response.status_code == 200:
            length = response.json()['length']
            chain = response.json()['chain']
            # Check if the length is longer and the chain is valid
            if length > max_length and self.valid_chain(chain):
                max_length = length
                new_chain = chain
    # Replace our chain if we discovered a new, valid chain longer than ours
    if new_chain:
        self.chain = new_chain
        return True
    return False

   def valid_chain(chain):
    last_block = chain[0]
    current_index = 1

    while current_index < len(chain):
        block = chain[current_index]
        #print(last_block)
        #print(block)
       #print("\n-----------\n")
        # Check that the hash of the block is correct
        if block['previous_hash'] != self.hash(last_block):
            return False
        # Check that the Proof of Work is correct
        #Delete the reward transaction
        transactions = block['transactions'][:-1]
        # Need to make sure that the dictionary is ordered. Otherwise we'll get a different hash
        transaction_elements = ['sender_address', 'recipient_address', 'value']
        transactions = [OrderedDict((k, transaction[k]) for k in transaction_elements) for transaction in transactions]
        if not self.valid_proof(transactions, block['previous_hash'], block['nonce'], MINING_DIFFICULTY):
            return False
        last_block = block
        current_index += 1
    return True
'''

@app.route('/sync-chain', methods=['GET'])
def consensus():
    def get_neighbour_chains():
        neighbour_chains = []
        for node_address in blockchain.nodes:
            resp = requests.get(node_address + url_for('get_full_chain')).json()
            chain = resp['chain']
            neighbour_chains.append(chain)
        return neighbour_chains
    neighbour_chains = get_neighbour_chains()
    
    if not neighbour_chains:
        return jsonify({'message': 'No neighbour chain is available'})
    longest_chain = max(neighbour_chains, key=len)  # Get the longest chain
    if len(blockchain.chain) > len(longest_chain):  # If our chain is longest, then do nothing
        response = {    
            'message': 'Chain is already up to date',
            'chain': blockchain.get_serialized_chain
        }
    else:  # If our chain isn't longest, then we store the longest chain
        blockchain.chain = [blockchain.get_block_object_from_block_data(block) for block in longest_chain]
        response = {
            'message': 'Chain was replaced',
            'chain': blockchain.get_serialized_chain
        }
        
    return jsonify(response)
'''
@app.route('/sync-chain', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }
    return jsonify(response), 200
'''
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-H', '--host', default='127.0.0.1')
    parser.add_argument('-p', '--port', type=int)
    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=True)
