# node.py
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from block import Block
from src.common.owner import Owner


class Node:
    def __init__(self, blockchain: Block):
        self.blockchain = blockchain

    @staticmethod
    def validate_signature(public_key: bytes, signature: bytes, transaction_data: bytes):
        public_key_object = RSA.import_key(public_key)
        transaction_hash = SHA256.new(transaction_data)
        pkcs1_15.new(public_key_object).verify(transaction_hash, signature)

    @staticmethod
    def create_wallet() -> dict:
        owner = Owner()
        return {
            "public_key": owner.public_key_hex,
            "public_key_hash": owner.public_key_hash,
            "private_key": str(owner.private_key.export_key(format="DER")),
        }
