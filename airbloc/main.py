# This is a pseudo-code implementation of Airbloc Data Producer.
from airbloc.database.bigchaindb import BigchainDBConnection
from airbloc.database.datastore import DataStore
from airbloc.encrypt import Encryptor
from airbloc.pseudo import cleanse, blockchain_table, broadcast_to_pre
from airbloc.config import Config
from base64 import b64decode
from airbloc.proto import AddDataResult, producer_pb2_grpc
from concurrent import futures
import grpc
import json
import time

config = Config('config.json')
bdb = BigchainDBConnection(bigchaindb_endpoint=config.bigchaindb_endpoint,
                           mongo_endpoint=config.mongo_endpoint)
datastore = DataStore(bdb)
encryptor = Encryptor(b'SafeSafeSafeSafe', b'FundszAreSafeMan')


def on_access_request(requestor_pubkey: str, data_id: str):
    """ Re-Encryption Node requests access.
    request_addr is data consumer's Ethereum address, and also public key.
    """
    pubkey = b64decode(requestor_pubkey)
    data = datastore.get(data_id)

    if not blockchain_table['data_id'].get(requestor_pubkey):
        return 'Failed'

    kfrags = encryptor.reencrypt(pubkey)
    broadcast_to_pre(kfrags, topic=data.capsule)
    return 'Succeed'


class ProducerServicer(producer_pb2_grpc.ProducerServicer):
    def AddData(self, data_stream, context):
        """ Cleanse the data and store the data on datastore. """
        for data in data_stream:
            # At the alpha version, we don't use AID and identity matcher yet.
            # so we'll make an assumption that provider will always give user ID.
            owner_id = data.ownerIdentifier.identifier
            payload = cleanse(data.payload)

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
