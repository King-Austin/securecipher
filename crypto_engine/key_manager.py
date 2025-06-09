from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

class KeyManager:
    def generate_ecdsa_key_pair(self):
        private_key = ec.generate_private_key(ec.SECP384R1())
        public_key = private_key.public_key()
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        return private_pem.decode(), public_pem.decode()
