from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
import db

env_directory = "../.env"
load_dotenv(dotenv_path=env_directory)

class Encrypt():
    def __init__(self):
        self.key = os.environ.get("ENCRYPTION_KEY")

        if self.key is None:
            raise ValueError("Encryption key was not found in the environment variable. ")

        self.key = self.key.encode()

        self.cipher_suite = Fernet(self.key)

    def encrypt(self, phrase):
        return self.cipher_suite.encrypt(phrase.encode())

    def decrypt(self, phrase):
        return self.cipher_suite.decrypt(phrase).decode()
    
## make a function to transition and switch encryption keys