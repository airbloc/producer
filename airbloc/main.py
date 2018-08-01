# This is a pseudo-code implementation of Airbloc Data Producer.
import json
import time
from concurrent import futures

import grpc

from airbloc.config import Config
from airbloc.blockchain import Contracts
from airbloc.crypto import Encryptor, Key
from airbloc.data import Cleanser
from airbloc.database import BigchainDBConnection, DataStore, Metadatabase
from airbloc.proto import AddDataResult, producer_pb2_grpc

config = Config('config.json')

private_key = Key.load_file(config.private_key_path)
encryptor = Encryptor(private_key)

bdb = BigchainDBConnection(bigchaindb_endpoint=config.bigchaindb_endpoint,
                           mongo_endpoint=config.mongo_endpoint,
                           credential=private_key.get_bigchaindb_keypair())
datastore = DataStore(bdb)
metadatabase = Metadatabase(bdb)

contracts = Contracts(deployment_path=config.contract_deployment_path,
                      abi_path=config.contract_abi_path,
                      provider_uri=config.ethereum_provider_uri)
cleanser = Cleanser(metadatabase, contracts)


class ProducerServicer(producer_pb2_grpc.ProducerServicer):

    def AddData(self, data_stream, context):
        """ Cleanse the data and store the data on datastore. """
        for data in data_stream:
            # At the alpha version, we don't use AID and identity matcher yet.
            # so we'll make an assumption that provider will always give user ID.
            owner_id = data.ownerIdentifier.identifier
            payload = cleanser.cleanse(category_id=data.categoryOfApp,
                                       user_aid=owner_id,
                                       data=json.loads(data.payload))

            plaintext = bytes(json.dumps(payload), 'utf-8')
            enc_payload, capsule = encryptor.encrypt(plaintext)

            data_id = datastore.store(data=enc_payload,
                                      owner_aid=owner_id,
                                      category=data.categoryOfApp,
                                      capsule=capsule.to_bytes())

            yield AddDataResult(dataId=data_id)


def serve(max_workers: int, port: int):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers))
    producer_pb2_grpc.add_ProducerServicer_to_server(ProducerServicer(), server)

    print('Listening on port localhost:{}'.format(port))
    server.add_insecure_port('[::]:{}'.format(port))
    server.start()

    try:
        # since gRPC server doesn't block, halt the main thread manually
        while True:
            time.sleep(10000)
    except KeyboardInterrupt:
        server.stop(0)
