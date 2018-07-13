from airbloc.database.bigchaindb import BigchainDBConnection
from base64 import b64encode
import time

class DataStore:
    """ Data warehouse implementation.
        During the MVP, we'll use BigchainDB as our (centralized) DW."""

    def __init__(self, bigchaindb: BigchainDBConnection):
        self.bdb = bigchaindb
    
    def store(self, data: str, capsule: bytes, category: str) -> str:
        payload = {
            'createdAt': int(time.time()),
            'category': category,
            'keyCapsule': b64encode(capsule),
            'data': data
        }
        return self.bdb.create(payload)
    
    def get(self, id: str):
        return self.bdb.retrieveById(id)