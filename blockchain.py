import time
import hashlib
import datetime

class Block(object):

    def __init__(self, index, proof, previous_hash, transactions):
        self.index = index #index of the block in blockchain list
        self.proof = proof #block is generated using this proof
        self.previous_hash = previous_hash #hash of the previous block in blockchain
        self.transactions = transactions #list of all transactions
        self.timestamp = time.time()
        self.originaltime = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')

    @property
    def get_block_hash(self): #calculates the hash based on the above attributes
        block_string = "{} - {} - {} - {} - {}".format(self.index, self.proof, self.previous_hash, self.transactions, self.originaltime)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def __repr__(self):
        return "{} - {} - {} - {} - {}".format(self.index, self.proof, self.previous_hash, self.transactions, self.originaltime)

class BlockChain(object):

    def __init__(self):
        self.chain = []  #holds all the blocks
        self.current_node_transactions = []  #store all transactions which will be inserted into the block
        self.nodes = set()
        self.create_genesis_block() #creating genesis block

    @property
    def get_serialized_chain(self): #Gets the chain from the asked server/node
        return [vars(block) for block in self.chain]

    def create_genesis_block(self): #Creates the genesis(first/default) block
        self.create_new_block(proof=0, previous_hash=0)

    def create_new_block(self, proof, previous_hash): #Creates new block
        block = Block(
            index=len(self.chain),
            proof=proof,
            previous_hash=previous_hash,
            transactions=self.current_node_transactions
        )
        self.current_node_transactions = []  #Reset the transaction list

        self.chain.append(block) #appending newly created block ot the chain
        return block

    @staticmethod
    def is_valid_block(block, previous_block): #Checks the block whether valid or not
        if previous_block.index + 1 != block.index:
            return False

        elif previous_block.get_block_hash != block.previous_hash:
            return False

        elif not BlockChain.is_valid_proof(block.proof, previous_block.proof):
            return False

        elif block.timestamp <= previous_block.timestamp:
            return False

        return True

    def create_new_transaction(self, sender, recipient, amount): #Creates new transaction
        self.current_node_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        return True

    @staticmethod
    def is_valid_transaction():   #Checks the transaction whether valid or not
        # Still to be implemented
        pass

    @staticmethod 
    def create_proof_of_work(previous_proof): #Creates proof of work algorithm
        proof = previous_proof + 1
        while not BlockChain.is_valid_proof(proof, previous_proof):
            proof += 1

        return proof

    @staticmethod
    def is_valid_proof(proof, previous_proof): #Checks valid proof
        return (proof + previous_proof) % 10 == 0

    @property 
    def get_last_block(self): #Gets last block
        return self.chain[-1]

    def is_valid_chain(self): #checks valid chain
        previous_block = self.chain[0]
        current_index = 1
        while current_index < len(self.chain):
            block = self.chain[current_index]
            if not self.is_valid_block(block, previous_block):
                return False
            previous_block = block
            current_index += 1
        return True
    
    def mine_block(self, miner_address): #Mines the block into the chain
        '''
        self.create_new_transaction(
            sender="Harsha",
            recipient=miner_address,
            amount=22000,
        )
        '''
        last_block = self.get_last_block
        last_proof = last_block.proof
        proof = self.create_proof_of_work(last_proof)
        last_hash = last_block.get_block_hash
        block = self.create_new_block(proof, last_hash)
        return vars(block)  # Return a native Dict type object
    
    
    def create_node(self, address): #Creates new node
        self.nodes.add(address)
        return True

    @staticmethod
    def get_block_object_from_block_data(block_data): #Calls specidic block from the chain when called
        return Block(
            block_data['index'],
            block_data['proof'],
            block_data['previous_hash'],
            block_data['transactions'],
            #timestamp = block_data['timestamp'],
            #originaltime=block.data['originaltime']
        )
