from airbloc.database.bigchaindb import BigchainDBConnection

class Metadatabase:

    def __init__(self):
        self.conn = BigchainDBConnection()

    def get(self, type: str, id: str) -> dict:
        query = {
            'data.type': type,
            '_id': id
        }
        return self.conn.retrieve_one(query)
