from airbloc.database.bigchaindb import BigchainDBConnection
import time

class DataStore:
    """ Data warehouse implementation.
        During the MVP, we'll use BigchainDB as our (centralized) DW."""

    def __init__(self, bigchaindb: BigchainDBConnection):
        self.bdb = bigchaindb
    
    def store(self, data: str, category: str) -> str:
        payload = {
            'createdAt': int(time.time()),
            'category': category,
            'data': data
        }
        return self.bdb.create(payload)
    