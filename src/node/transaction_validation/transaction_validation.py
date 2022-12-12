# node.py
import binascii
import logging

import requests
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from config import PUBLIC_KEY
from src.common.owner import Owner
from ...common.block import Block
from ...common.io_known_nodes import KnownNodesMemory
from ...common.io_mem_pool import MemPool


class TransactionException(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class Transaction:
    def __init__(self, blockchain: Block, hostname: str):
        self.blockchain = blockchain
        self.transaction_data: dict = {}
        self.transaction_hash: bytes = b""
        self.signature: bytes = b""
        self.is_valid = False
        self.mempool = MemPool()
        self.known_node_memory = KnownNodesMemory()
        self.sender = ""
        self.hostname = hostname

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

    def validate(self):
        public_key_object = RSA.import_key(PUBLIC_KEY)
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
        logging.info("Broadcasting to all nodes")
        node_list = self.known_node_memory.known_nodes
        for node in node_list:
            if node.hostname != self.hostname and node.hostname != self.sender:
                try:
                    logging.info(f"Broadcasting to {node.hostname}")
                    node.send_transaction(self.transaction_data)
                except requests.ConnectionError:
                    logging.info(f"Failed broadcasting to {node.hostname}")

    def store(self):
        if self.is_valid:
            logging.info("Storing transaction data in memory")
            logging.info(f"Transaction data: {self.transaction_data}")
            current_transaction = self.mempool.get_transactions_from_memory()
            current_transaction.append(self.transaction_data)
            self.mempool.store_transactions_in_memory(current_transaction)
