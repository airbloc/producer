# This is a pseudo-code implementation of Airbloc Data Producer.
from airbloc.database.bigchaindb import BigchainDBConnection
from airbloc.database.metadatabase import Metadatabase
from airbloc.database.datastore import DataStore
from airbloc.encrypt import Encryptor
from airbloc.pseudo import cleanse
import json

bdb = BigchainDBConnection()
datastore = DataStore(bdb)
encryptor = Encryptor(b'SafeSafeSafeSafe', b'FundszAreSafeMan')

def process(data: dict):
    data = cleanse(data)
    enc_data, capsule = encryptor.encrypt(data)
    datastore.store(enc_data, capsule, 'installed-apps')

def main():
    # just test, lol.
    process({ 'installedApps': [{ 'package': 'io.airbloc.wallet', 'installedAt': 3032903284 }] })
