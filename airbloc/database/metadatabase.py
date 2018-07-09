from airbloc.database.bigchaindb import BigchainDBConnection

class Metadatabase:

    def __init__(self):
        self.conn = BigchainDBConnection()
    