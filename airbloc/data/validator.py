import fastjsonschema
from airbloc.database import Metadatabase


class Validator(object):

    def __init__(self, metadb: Metadatabase):
        self._validator_cache = dict()
        self._metadb = metadb

    def validate_schema(self, category_id, data) -> object:
        """ Validate given data. """

        if category_id not in self._validator_cache:
            # fetch schema from metadatabase (blockchain, BigchainDB)
            category_of_app = self._metadb.get('CategoryOfApp', category_id)
            category = self._metadb.get('Category', category_of_app['category'])

            validator = fastjsonschema.compile(category['schema'])
            self._validator_cache[category_id] = validator

        validator = self._validator_cache[category_id]
        return validator(data)