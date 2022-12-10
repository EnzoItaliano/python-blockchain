# node.py
import binascii

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from src.common.owner import Owner
from .block import Block


class Node:
    def __init__(self, blockchain: Block):
        self.blockchain = blockchain

    @staticmethod
    def validate_signature(public_key: bytes, signature: bytes, transaction_data: bytes):
        public_key_object = RSA.import_key(public_key)
        transaction_hash = SHA256.new(transaction_data)
        pkcs1_15.new(public_key_object).verify(transaction_hash, binascii.unhexlify(signature))

    @staticmethod
    def create_wallet() -> dict:
        owner = Owner()
        return {
            "public_key": owner.public_key.decode("utf-8"),
            "private_key": owner.private_key.export_key().decode("utf-8"),
        }
