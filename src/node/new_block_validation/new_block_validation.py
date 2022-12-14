import logging

import requests

from src.common.block import Block, BlockHeader
from src.common.io_blockchain import BlockchainMemory
from src.common.io_known_nodes import KnownNodesMemory
from src.common.io_mem_pool import MemPool
from src.common.values import NUMBER_OF_LEADING_ZEROS
from src.node.transaction_validation.transaction_validation import Transaction


class NewBlockException(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class NewBlock:
    def __init__(self, blockchain: Block, hostname: str):
        self.blockchain = blockchain
        self.new_block = None
        self.sender = ""
        self.mempool = MemPool()
        self.known_nodes_memory = KnownNodesMemory()
        self.blockchain_memory = BlockchainMemory()
        self.hostname = hostname

    def receive(self, new_block: dict, sender: str):
        new_block["header"].pop("hash")
        block_header = BlockHeader(**new_block["header"])
        self.new_block = Block(transaction=new_block["transaction"], block_header=block_header)
        self.sender = sender
        try:
            assert (
                self.blockchain.block_header.hash
                == self.new_block.block_header.previous_block_hash
            )
        except AssertionError:
            print("Previous block provided is not the most recent block")
            raise NewBlockException("", "Previous block provided is not the most recent block")

    def validate(self):
        self._validate_hash()
        self._validate_transactions()

    def _validate_hash(self):
        new_block_hash = self.new_block.block_header.get_hash()
        number_of_zeros_string = "".join([str(0) for _ in range(NUMBER_OF_LEADING_ZEROS)])
        try:
            assert new_block_hash.startswith(number_of_zeros_string)
        except AssertionError:
            print("Proof of work validation failed")
            raise NewBlockException("", "Proof of work validation failed")

    def _validate_transactions(self):
        transaction = Transaction(self.blockchain, self.hostname)
        transaction.receive(transaction=self.new_block.transaction)
        transaction.validate()

    def add(self):
        self.new_block.previous_block = self.blockchain
        self.blockchain_memory.store_blockchain_in_memory(self.new_block)

    def clear_block_transactions_from_mempool(self):
        # self.mempool.clear_first_transaction_from_memory()

        current_transactions = self.mempool.get_transactions_from_memory()
        transactions_cleared = []
        for current_transaction in current_transactions:
            if not (current_transaction == self.new_block.transaction):
                transactions_cleared.append(current_transaction)
        self.mempool.store_transactions_in_memory(transactions_cleared)

    def broadcast(self):
        logging.info(f"Broadcasting block")
        node_list = self.known_nodes_memory.known_nodes
        for node in node_list:
            if node.hostname != self.hostname and node.hostname != self.sender:
                block_content = {
                    "block": {
                        "header": self.new_block.block_header.to_dict,
                        "transaction": self.new_block.transaction,
                    },
                    "sender": self.hostname,
                }
                try:
                    logging.info(f"Broadcasting to {node.hostname}")
                    node.send_new_block(block_content)
                except requests.exceptions.HTTPError as error:
                    logging.info(f"Failed to broadcast block to {node.hostname}: {error}")
