from umbral import keys
from bigchaindb_driver.crypto import CryptoKeypair
from cryptoconditions.crypto import Ed25519SigningKey

class Key(object):

    def __init__(self, key: bytes):
        self.key = key

    @classmethod
    def generate(cls) -> 'Key':
        """ Generate new ECDSA key.
        :return: Generated key bytes
        """
        key = keys.UmbralPrivateKey.gen_key().to_bytes()
        return cls(key)

    @classmethod
    def load_file(cls, path) -> 'Key':
        with open(path, mode='r') as file:
            key_hex = file.read()

        if len(key_hex) != 64:
            raise AssertionError('Wrong key format. Is it an ECDSA key with SECP256K1 curve?')

        key = bytes.fromhex(key_hex)
        return cls(key)

    def save(self, path: str):
        """ Saves the key. """
        with open(path, mode='w') as file:
            file.write(self.key.hex())

    def to_bytes(self):
        return self.key

    def get_bigchaindb_keypair(self) -> CryptoKeypair:
        # using self.key as a private key.
        private_key = Ed25519SigningKey(self.key, encoding='bytes')
        public_key = private_key.get_verifying_key()

        return CryptoKeypair(private_key=private_key.encode(),
                             public_key=public_key.encode())

