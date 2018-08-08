import fastjsonschema
from airbloc.database import Metadatabase


class SchemaRegistry(object):

    def __init__(self, metadb: Metadatabase):
        self._validator_cache = dict()
        self._metadb = metadb

    def register(self, name, schema: dict) -> str:
        # TODO: make payable
        validator = fastjsonschema.compile(schema)

        payload = {
            'name': name,
            'schema': schema,
        }
        schema_id = self._metadb.create('Schema', payload)
        self._validator_cache[schema_id] = validator
        return schema_id

    def list(self, query=None, limit=-1, page=0):
        if query is None:
            query = {}

        return self._metadb.query(query, limit=limit, page=page)

    def validate(self, category_id, data) -> object:
        """ Validate given data. """

        if category_id not in self._validator_cache:
            # fetch schema from metadatabase (blockchain, BigchainDB)
            category_of_app = self._metadb.get('CategoryOfApp', category_id)
            schema = self._metadb.get('Schema', category_of_app['schemaId'])

            # TODO: check that schema is registered in blockchain

            validator = fastjsonschema.compile(schema['schema'])
            self._validator_cache[category_id] = validator

        validator = self._validator_cache[category_id]
        return validator(data)
