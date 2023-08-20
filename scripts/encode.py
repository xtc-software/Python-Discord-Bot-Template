import base64
import os
from cryptography.hazmat.primitives import serialization, hashes, padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

async def encode(string: str):
    string_bytes = string.encode("ascii")
    b64_bytes = base64.urlsafe_b64encode(string_bytes)
    b64_string = b64_bytes.decode("ascii")
    return b64_string

async def decode(string: str):
    b64_bytes = string.encode("ascii")
    decoded_bytes = base64.urlsafe_b64decode(b64_bytes)
    decoded_string = decoded_bytes.decode("ascii")
    return decoded_string

class AdvancedEncryptor:
    def __init__(self, kek_password):
        self.kek_password = kek_password.encode('utf-8')
        self.kek = None  # Key Encryption Key
        self.generate_kek()

    def generate_kek(self):
        # Generate a salt for PBKDF2
        salt = os.urandom(16)
        
        # Create a Key Derivation Function (KDF) instance with SHA256
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            iterations=100000,  # Number of iterations
            salt=salt,  # Salt for added security
            length=32  # Desired key length
        )
        
        # Derive the KEK from the provided password using PBKDF2
        kek_key = kdf.derive(self.kek_password)
        self.kek = kek_key

    def encrypt(self, plaintext):
        # Generate a new Data Encryption Key (DEK) for each encryption
        dek = os.urandom(32)  # Random DEK
        iv = os.urandom(16)   # Initialization vector for AES in CFB mode
        
        # Create an AES cipher in CFB mode with the generated DEK and IV
        cipher = Cipher(algorithms.AES(dek), modes.CFB(iv))
        encryptor = cipher.encryptor()
        
        # Encrypt the plaintext using the AES cipher
        ct = encryptor.update(plaintext.encode('utf-8')) + encryptor.finalize()

        # Encrypt the DEK with the KEK using RSA
        rsa_private_key = serialization.load_pem_private_key(self.kek)
        encrypted_dek = rsa_private_key.public_key().encrypt(
            dek,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Combine the encrypted DEK, IV, and ciphertext for storage or transmission
        return encrypted_dek + iv + ct

    def decrypt(self, ciphertext):
        # Separate the encrypted DEK, IV, and ciphertext from the input
        encrypted_dek = ciphertext[:256]  # Assuming RSA encrypted DEK is 256 bytes
        iv = ciphertext[256:272]
        ct = ciphertext[272:]

        # Decrypt the DEK with the KEK using RSA
        rsa_private_key = serialization.load_pem_private_key(self.kek)
        dek = rsa_private_key.decrypt(
            encrypted_dek,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Create an AES cipher in CFB mode with the decrypted DEK and IV
        cipher = Cipher(algorithms.AES(dek), modes.CFB(iv))
        decryptor = cipher.decryptor()
        
        # Decrypt the ciphertext using the AES cipher
        pt = decryptor.update(ct) + decryptor.finalize()

        return pt.decode('utf-8')


def main():
    kek_password = "YourSuperSecretKEKPassword"
    encryptor = AdvancedEncryptor(kek_password)

    original_text = "Hello, this is a secret message!"
    
    # Encrypt the original text
    encrypted_text = encryptor.encrypt(original_text)
    
    # Decrypt the encrypted text
    decrypted_text = encryptor.decrypt(encrypted_text)

    print("Original Text:", original_text)
    print("Encrypted Text:", encrypted_text)
    print("Decrypted Text:", decrypted_text)


if __name__ == "__main__":
    main()
