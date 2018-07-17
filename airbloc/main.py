# This is a pseudo-code implementation of Airbloc Data Producer.
from airbloc.database.bigchaindb import BigchainDBConnection
from airbloc.database.datastore import DataStore
from airbloc.encrypt import Encryptor
from airbloc.pseudo import cleanse, blockchain_table, broadcast_to_pre, identity_match_request
from base64 import b64decode
from airbloc.proto import ProducerServicer, AddDataSummary, producer_pb2_grpc
from concurrent import futures
import grpc
import json
import time

bdb = BigchainDBConnection()
datastore = DataStore(bdb)
encryptor = Encryptor(b'SafeSafeSafeSafe', b'FundszAreSafeMan')

def process(data: dict):
    data = cleanse(data)
    enc_data, capsule = encryptor.encrypt(data)
    datastore.store(enc_data, capsule, 'installed-apps')

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

class ProducerServicerImpl(ProducerServicer):

    def AddData(self, data_stream, context):
        inserted_count = 0
        start_time = time.time()

        for data in data_stream:
            owner_id = identity_match_request(data.ownerIdentifier)
            payload = cleanse(data.payload)

            plaintext = json.dumps(payload)
            enc_payload, capsule = encryptor.encrypt(plaintext)

            datastore.store(enc_payload, capsule, data.categoryOfApp)
            inserted_count += 1

        elapsed_time = time.time() - start_time
        return AddDataSummary(insertedCount=inserted_count,
                              elaspedTime=elapsed_time)

def serve(max_workers: int, port: int):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers))
    producer_pb2_grpc.add_ProducerServicer_to_server(ProducerServicerImpl(), server)

    print('Listening on port localhost:{}'.format(port))
    server.add_insecure_port('[::]:{}'.format(port))
    server.start()

    try:
        # since gRPC server doesn't block, halt the main thread manually
        while True:
            time.sleep(10000)
    except KeyboardInterrupt:
        server.stop(0)
