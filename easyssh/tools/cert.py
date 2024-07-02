import paramiko
import os


class cert:
    def __init__(self, private_key_path):
        self.private_key_path = private_key_path

    def create(self):
        key = paramiko.RSAKey.generate(1024)
        key.write_private_key_file(self.private_key_path)

    def delete(self):
        os.remove(self.private_key_path)
