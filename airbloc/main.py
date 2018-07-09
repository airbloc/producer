# This is a pseudo-code implementation of Airbloc Data Producer.
from airbloc.database.bigchaindb import BigchainDBConnection
from airbloc.database.metadatabase import Metadatabase
from airbloc.database.datastore import DataStore
from airbloc.pseudo import encrypt, cleanse

import json

bdb = BigchainDBConnection()
datastore = DataStore(bdb)

def process(data: dict) -> str:
    data = cleanse(data)
    enc_data = encrypt(data)
    datastore.store(enc_data, 'installed-apps')
    # TODO: re-key and send to KMS.
    # TODO: inter-node communication

def main():
    pass