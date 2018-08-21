from .identity import Identity
from airbloc.database import LevelDBModel, LevelDBConnection
from typing import List

class IdentityMatcher:

    def __init__(self, db_connection: LevelDBConnection):
        self._db = LevelDBModel('id', connection=db_connection)

    def query(self, identities: List[Identity]) -> Identity:
        # TODO: using RPC
        pass
