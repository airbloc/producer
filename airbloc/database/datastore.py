from airbloc.database.bigchaindb import BigchainDBConnection
from base64 import b64encode
import time

def b64encode_str(s: bytes) -> str:
    return b64encode(s).decode('utf-8')

class DataStore:
    """ Data warehouse implementation.
        During the MVP, we'll use BigchainDB as our (centralized) DW."""

    def __init__(self, bigchaindb: BigchainDBConnection):
        self.bdb = bigchaindb
    
    def store(self, data: bytes, owner_aid: str, capsule: bytes, category: str) -> str:
        payload = {
            'createdAt': int(time.time()),
            'ownerAid': owner_aid,
            'category': category,
            'data': {
                'payload': b64encode_str(data),
                'keyCapsule': b64encode_str(capsule)
            }
        }
        print(payload)
        return self.bdb.create(payload)
    
    def get(self, id: str):
        return self.bdb.retrieve_by_id(id)