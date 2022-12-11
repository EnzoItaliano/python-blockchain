# node.py
import binascii

import requests
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from src.common.owner import Owner
from ...common.block import Block
from ...common.io_mem_pool import MemPool
from ...common.node import Node


class OtherNode(Node):
    def __init__(self, ip: str, port: int):
        super().__init__(ip, port)

    def send_transaction(self, transaction_data: dict) -> requests.Response:
        return self.post("add", transaction_data)


class Transaction:
    def __init__(self, blockchain: Block = None):
        self.blockchain = blockchain
        self.transaction_data: dict = {}
        self.transaction_hash: bytes = b""
        self.signature: bytes = b""
        self.is_valid = False
        self.mempool = MemPool()

    @staticmethod
    def create_wallet() -> dict:
        owner = Owner()
        return {
            "public_key": owner.public_key.decode("utf-8"),
            "private_key": owner.private_key.export_key().decode("utf-8"),
        }

    def receive(self, transaction: dict):
        self.transaction_data = transaction
        self.transaction_hash = bytes(transaction["transaction_hash"], "utf-8")
        self.signature = bytes(transaction["signature"], "utf-8")

    def validate(self, public_key: bytes):
        public_key_object = RSA.import_key(public_key)
        transaction_hash = SHA256.new(self.transaction_hash)
        if (
            pkcs1_15.new(public_key_object).verify(
                transaction_hash, binascii.unhexlify(self.signature)
            )
            is None
        ):
            self.is_valid = True

    @property
    def is_new(self):
        current_transactions = self.mempool.get_transactions_from_memory()
        if self.transaction_data in current_transactions:
            return False
        return True

    def broadcast(self):
        node_list = [
            OtherNode("localhost", 5001),
            OtherNode("localhost", 5002),
        ]
        for node in node_list:
            try:
                node.send_transaction(self.transaction_data)
            except requests.ConnectionError:
                pass

    def store(self):
        if self.is_valid:
            current_transaction = self.mempool.get_transactions_from_memory()
            current_transaction.append(self.transaction_data)
            self.mempool.store_transaction_in_memory(current_transaction)
