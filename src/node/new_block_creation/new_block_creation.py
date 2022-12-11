import json
from datetime import datetime

import requests

from src.common.block import Block, BlockHeader
from src.common.io_blockchain import BlockchainMemory
from src.common.io_mem_pool import MemPool
from src.common.node import Node
from src.common.utils import calculate_hash
from src.common.values import NUMBER_OF_LEADING_ZEROS


class BlockException(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class OtherNode(Node):
    def __init__(self, ip: str, port: int):
        super().__init__(ip, port)

    def send_new_block(self, block: dict) -> requests.Response:
        return self.post(endpoint="block", data=block)


class ProofOfWork:
    def __init__(self):
        blockchain_memory = BlockchainMemory()
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
        node_list = [OtherNode("localhost", 5000)]
        for node in node_list:
            block_content = {
                "block": {
                    "header": self.new_block.block_header.to_dict,
                    "transaction": self.new_block.transaction,
                }
            }
            node.send_new_block(block_content)
