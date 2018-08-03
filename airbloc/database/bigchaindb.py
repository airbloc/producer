from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair
from pymongo import MongoClient

_DEFAULT_BIGCHAINDB_ENDPOINT = 'http://localhost:9984'
_DEFAULT_MONGO_ENDPOINT = 'mongo://localhost:27017'
_BURN_ADDRESS = 'BurnBurnBurnBurnBurnBurnBurnBurnBurnBurnBurn'

class BigchainDBConnection:
    """ Implements basic CRAB (Create-Retrieve-Append-Burn) 
        and advanced query interfaces for BigchainDB."""

    def __init__(self,
            bigchaindb_endpoint=_DEFAULT_BIGCHAINDB_ENDPOINT,
            mongo_endpoint=_DEFAULT_MONGO_ENDPOINT,
            credential=generate_keypair()):
        
        self.bdb = BigchainDB(bigchaindb_endpoint)
        self.mdb = MongoClient(mongo_endpoint)['bigchain']
        self.key = credential
        self.transaction_history = []

    def _send_transaction(self, prepared_tx, private_keys=None):
        if private_keys == None:
            # default owner is me
            private_keys = self.key.private_key
        
        tx = self.bdb.transactions.fulfill(prepared_tx, private_keys=private_keys)
        self.bdb.transactions.send_commit(tx)
        self.transaction_history.append(tx)
        return tx
    
    def get_transaction(self, txid):
        for i in range(len(self.transaction_history), 0, -1):
            tx = self.transaction_history[i]
            if tx['id'] == txid:
                return tx

        # not found in history, so let's query some TX
        return self.bdb.transactions.retrieve(txid)

    def create(self, data, metadata=None):
        prepared_tx = self.bdb.transactions.prepare(
                operation='CREATE',
                signers=self.key.public_key,
                asset={ 'data': data },
                metadata=metadata)
        
        tx = self._send_transaction(prepared_tx)
        return tx['id']

    def append(self, id, metadata, transfer_to=None):
        ''' Appends the metadata to asset.
            :param id ID of the data you want to update.
            :param metadata Payload of the data will be changed to.
        '''
        if transfer_to == None:
            # transfer to myself = just append things.
            transfer_to = self.key.public_key

        tx = self.get_transaction(id)

        output_index = 0
        output = tx['outputs'][output_index]
        inputs = {
            'fulfillment': output['condition']['details'],
                'fulfills': {
                'output_index': output_index,
                'transaction_id': id,
            },
            'owners_before': output['public_keys'],
        }
        prepared_tx = self.bdb.transactions.prepare(
                operation='TRANSFER',
                inputs=inputs,
                asset={ 'id': id },
                metadata=metadata)

        return self._send_transaction(prepared_tx, private_keys=transfer_to)
    
    def burn(self, id):
        ''' Removes the data.'''
        return self.append(id, { 'status': 'BURNED' }, transfer_to=_BURN_ADDRESS)

    def transfer(self, id, transfer_to, metadata=None):
        return self.append(id, metadata, transfer_to=transfer_to)

    def retrieve_many(self, query):
        return self.mdb.assets.find(query)
    
    def retrieve_one(self, query):
        doc = self.mdb.assets.find_one(query)
        return doc['data'] if doc else None

    def retrieve_by_id(self, id):
        return self.retrieve_one({'id': id})

    def query_metadata(self, query):
        return self.mdb.metadata.find(query)


