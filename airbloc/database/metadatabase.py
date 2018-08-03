from airbloc.database.bigchaindb import BigchainDBConnection

class Metadatabase:

    def __init__(self, conn: BigchainDBConnection):
        self._bdb = conn

    def create(self, type: str, payload: dict) -> str:
        created_at = self._bdb.create({
            'type': type,
            'payload': payload,
        })
        return created_at

    def get(self, type: str, id: str) -> dict:
        query = {
            'data.type': type,
            'id': id,
        }
        data = self._bdb .retrieve_one(query)
        return data['payload'] if data else None
