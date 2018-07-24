import fastjsonschema
from typing import Callable

class Cleanser(object):

    def __init__(self, schema_fetcher: Callable[[str], object]):
        self._fetch_schema = schema_fetcher
        self._validator_cache = dict()

    def validate_schema(self, schema_id: str, data: object) -> object:
        """ Validate given data. """

        if schema_id not in self._validator_cache:
            # fetch schema from blockchain
            schema = self._fetch_schema(schema_id)
            validator = fastjsonschema.compile(schema)
            self._validator_cache[schema_id] = validator

        validator = self._validator_cache[schema_id]
        return validator(data)

    def check_dauth(self, category_id: str, user_aid: str) -> bool:
        # TODO: implement DAuth
        return True

    def cleanse(self, category_id: str, user_aid: str, data: object) -> object:
        # 1. filter data that user hasn't authorized
        user_allowed = self.check_dauth(user_aid, category_id)
        if not user_allowed:
            raise AssertionError('User {} not allowed data {}'.format(user_aid, category_id))

        # 2. validate schema
        validated_data = self.validate_schema(category_id, data)
        return validated_data
