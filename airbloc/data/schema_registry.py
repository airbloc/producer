import fastjsonschema
from airbloc.database import Metadatabase


class SchemaRegistry(object):

    def __init__(self, metadb: Metadatabase):
        self._cache = dict()
        self._metadb = metadb

    def register(self, schema: dict) -> str:
        # TODO: make payable
        validator = fastjsonschema.compile(schema)
        schema_id = self._metadb.create('Schema', {'schema': schema})
        self._cache[schema_id] = validator
        return schema_id

    def validate(self, category_id, data) -> object:
        """ Validate given data. """

        if category_id not in self._cache:
            # fetch schema from metadatabase (blockchain, BigchainDB)
            category_of_app = self._metadb.get('CategoryOfApp', category_id)
            schema = self._metadb.get('Schema', category_of_app['schemaId'])

            # TODO: check that schema is registered in blockchain

            validator = fastjsonschema.compile(schema['schema'])
            self._cache[category_id] = validator

        validator = self._cache[category_id]
        return validator(data)
