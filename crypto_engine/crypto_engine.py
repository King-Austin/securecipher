from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
import base64
import json

class CryptoEngine:
    """What it does: Core cryptographic operations for SecureCipher using secp384r1"""
    
    @staticmethod
    def validate_ecdsa_public_key(public_key_data):
        """
        What it does: Validates ECDSA public key from WebCrypto API
        
        Args:
            public_key_data: Dict with 'x' and 'y' coordinates (base64url encoded)
            
        Returns:
            bool: True if valid secp384r1 public key
        """
        try:
            # What it does: Decode base64url coordinates
            x_bytes = base64.urlsafe_b64decode(public_key_data['x'] + '==')
            y_bytes = base64.urlsafe_b64decode(public_key_data['y'] + '==')
            
            # What it does: Verify coordinate lengths for secp384r1 (48 bytes each)
            if len(x_bytes) != 48 or len(y_bytes) != 48:
                return False
            
            # What it does: Create public key point on secp384r1 curve
            curve = ec.SECP384R1()
            x_int = int.from_bytes(x_bytes, 'big')
            y_int = int.from_bytes(y_bytes, 'big')
            
            # What it does: Verify point is on curve
            public_numbers = ec.EllipticCurvePublicNumbers(x_int, y_int, curve)
            public_key = public_numbers.public_key()
            
            return True
            
        except Exception as e:
            print(f"Key validation error: {e}")
            return False
    
    @staticmethod
    def ecdsa_verify(signature, message, public_key_coords):
        """
        What it does: Verify ECDSA signature using secp384r1
        
        Args:
            signature: Base64 encoded signature
            message: Message bytes that were signed
            public_key_coords: Dict with 'x' and 'y' coordinates
            
        Returns:
            bool: True if signature is valid
        """
        try:
            # What it does: Reconstruct public key from coordinates
            x_bytes = base64.urlsafe_b64decode(public_key_coords['x'] + '==')
            y_bytes = base64.urlsafe_b64decode(public_key_coords['y'] + '==')
            
            x_int = int.from_bytes(x_bytes, 'big')
            y_int = int.from_bytes(y_bytes, 'big')
            
            curve = ec.SECP384R1()
            public_numbers = ec.EllipticCurvePublicNumbers(x_int, y_int, curve)
            public_key = public_numbers.public_key()
            
            # What it does: Verify signature
            signature_bytes = base64.b64decode(signature)
            public_key.verify(signature_bytes, message, ec.ECDSA(hashes.SHA384()))
            
            return True
            
        except Exception as e:
            print(f"Signature verification error: {e}")
            return False
    
    @staticmethod
    def generate_server_keypair():
        """
        What it does: Generate server-side ECDSA keypair for co-signing
        
        Returns:
            tuple: (private_key, public_key_coords)
        """
        try:
            # What it does: Generate secp384r1 key pair
            private_key = ec.generate_private_key(ec.SECP384R1())
            public_key = private_key.public_key()
            
            # What it does: Extract coordinates
            public_numbers = public_key.public_numbers()
            x_bytes = public_numbers.x.to_bytes(48, 'big')
            y_bytes = public_numbers.y.to_bytes(48, 'big')
            
            public_key_coords = {
                'x': base64.urlsafe_b64encode(x_bytes).decode().rstrip('='),
                'y': base64.urlsafe_b64encode(y_bytes).decode().rstrip('='),
                'crv': 'P-384',
                'kty': 'EC'
            }
            
            return private_key, public_key_coords
            
        except Exception as e:
            print(f"Server keypair generation error: {e}")
            return None, None