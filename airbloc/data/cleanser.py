from airbloc.blockchain import Contracts
from airbloc.database import Metadatabase
from .schema_registry import SchemaRegistry
from .dauth import DAuth

class Cleanser(object):

    def __init__(self, metadb: Metadatabase, contracts: Contracts):
        self._validator = SchemaRegistry(metadb)
        self._dauth = DAuth(contracts)

    def cleanse(self, category_id: str, user_aid: str, data: object) -> object:
        # 1. filter data that user hasn't authorized
        user_allowed = self._dauth.is_allowed(user_aid, category_id)
        if not user_allowed:
            raise AssertionError('User {} not allowed data {}'.format(user_aid, category_id))

        # 2. validate schema
        validated_data = self._validator.validate(category_id, data)
        return validated_data
