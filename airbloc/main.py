# This is a pseudo-code implementation of Airbloc Data Producer.
from airbloc.database.bigchaindb import BigchainDBConnection
from airbloc.database.metadatabase import Metadatabase
from airbloc.database.datastore import DataStore
from airbloc.encrypt import Encryptor
from airbloc.pseudo import cleanse, blockchain_table, broadcast_to_pre
from base64 import b64decode
import json

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

    if blockchain_table['data_id'].get(requestor_pubkey) == False:
        return 'Failed'
    
    kfrags = encryptor.reencrypt(pubkey)
    broadcast_to_pre(kfrags, topic=data.capsule)
    return 'Succeed'

def main():
    # just test, lol.
    process({ 'installedApps': [{ 'package': 'io.airbloc.wallet', 'installedAt': 3032903284 }] })
