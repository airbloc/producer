import plyvel

class LevelDBModel:

    def __init__(self, collection_name, connection):
        self._name = collection_name
        self._connection = connection

    def put(self, key: str, value: str):
        self._connection.put('{}-{}'.format(self._name, key), value)

    def get(self, key: str):
        return self._connection.get('{}-{}'.format(self._name, key))


class LevelDBConnection:

    def __init__(self, db_path):
        self._db = plyvel.DB(db_path, create_if_missing=True)

    def put(self, key: str, value: str):
        self._db.put(bytes_key=bytes(key, 'ascii'), value=bytes(value, 'utf-8'))

    def get(self, key: str) -> str:
        return self._db.get(bytes(key, 'ascii'))
