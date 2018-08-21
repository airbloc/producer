from .identity import Identity
from airbloc.database import LevelDBModel, LevelDBConnection
from typing import List

class IdentityMatcher:

    def __init__(self, db_connection: LevelDBConnection):
        self._db = LevelDBModel('id', connection=db_connection)

    def query(self, identities: List[Identity]) -> Identity:
        if len(identities) == 1:
            [identity] = identities
            return self._db.get(identity.name)
        pass

    def query_by_internal_user_id(self, internal_uid: str) -> str:
        pass
