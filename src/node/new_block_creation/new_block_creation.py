import json
import logging
from datetime import datetime

import requests

from src.common.block import Block, BlockHeader
from src.common.io_blockchain import BlockchainMemory
from src.common.io_known_nodes import KnownNodesMemory
from src.common.io_mem_pool import MemPool
from src.common.utils import calculate_hash
from src.common.values import NUMBER_OF_LEADING_ZEROS


class BlockException(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class ProofOfWork:
    def __init__(self, hostname: str):
        logging.info("Starting Proof of Work")
        self.known_nodes_memory = KnownNodesMemory()
        blockchain_memory = BlockchainMemory()
        self.hostname = hostname
        self.mem_pool = MemPool()
        self.blockchain = blockchain_memory.get_blockchain_from_memory()
        self.new_block = None

    @staticmethod
    def get_noonce(block_header: BlockHeader) -> int:
        block_header_hash = ""
        noonce = block_header.noonce
        starting_zeros = "".join([str(0) for _ in range(NUMBER_OF_LEADING_ZEROS)])
        while not block_header_hash.startswith(starting_zeros):
            noonce = noonce + 1
            block_header_content = {
                "previous_block_hash": block_header.previous_block_hash,
                "timestamp": block_header.timestamp,
                "noonce": noonce,
            }
            block_header_hash = calculate_hash(json.dumps(block_header_content))
        return noonce

    def create_new_block(self):
        transaction = self.mem_pool.get_first_transaction_from_memory()
        if transaction:
            block_header = BlockHeader(
                previous_block_hash=self.blockchain.block_header.hash,
                timestamp=datetime.timestamp(datetime.now()),
                noonce=0,
            )
            block_header.noonce = self.get_noonce(block_header)
            block_header.hash = block_header.get_hash()
            self.new_block = Block(transaction=transaction, block_header=block_header)
        else:
            raise BlockException("", "No transaction in mem_pool")

    def broadcast(self):
        logging.info("Broadcasting to other nodes")
        node_list = self.known_nodes_memory.known_nodes
        broadcasted_node = False
        for node in node_list:
            if node.hostname != self.hostname:
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
                    broadcasted_node = True
                except requests.exceptions.ConnectionError as e:
                    logging.info(f"Failed broadcasting to {node.hostname}: {e}")
                except requests.exceptions.HTTPError as e:
                    logging.info(f"Failed broadcasting to {node.hostname}: {e}")
        return broadcasted_node
