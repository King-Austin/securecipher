from django.test import TestCase
from .key_manager import KeyManager

class CryptoTest(TestCase):
    def test_key_generation(self):
        km = KeyManager()
        private_key, public_key = km.generate_ecdsa_key_pair()
        print("Private Key:", private_key)
        print("Public Key:", public_key)
        self.assertIn("BEGIN PUBLIC KEY", public_key)
