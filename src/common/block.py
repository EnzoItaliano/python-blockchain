import json

from src.common.utils import calculate_hash


class BlockHeader:
    def __init__(self, previous_block_hash: str, timestamp: float, noonce: int):
        self.previous_block_hash = previous_block_hash
        self.timestamp = timestamp
        self.noonce = noonce
        self.hash = self.get_hash()

    def __eq__(self, other):
        try:
            assert self.previous_block_hash == other.previous_block_hash
            assert self.timestamp == other.timestamp
            assert self.noonce == other.noonce
            assert self.hash == other.hash
            return True
        except AssertionError:
            return False

    def get_hash(self) -> str:
        header_data = {
            "previous_block_hash": self.previous_block_hash,
            "timestamp": self.timestamp,
            "noonce": self.noonce,
        }
        return calculate_hash(json.dumps(header_data))

    @property
    def to_dict(self) -> dict:
        return {
            "previous_block_hash": self.previous_block_hash,
            "timestamp": self.timestamp,
            "noonce": self.noonce,
            "hash": self.hash,
        }

    def __str__(self):
        return json.dumps(self.to_dict)

    @property
    def to_json(self) -> str:
        return json.dumps(self.to_dict)


class Block(object):
    def __init__(
        self,
        transaction: dict,
        block_header: BlockHeader,
        previous_block=None,
    ):
        self.transaction = transaction
        self.previous_block = previous_block
        self.block_header = block_header

    def __eq__(self, other):
        try:
            assert self.block_header == other.block_header
            assert self.transaction == other.transaction
            return True
        except AssertionError:
            return False

    def __len__(self) -> int:
        i = 1
        current_block = self
        while current_block.previous_block:
            i = i + 1
            current_block = current_block.previous_block
        return i

    def __str__(self):
        return json.dumps(
            {
                "timestamp": self.block_header.timestamp,
                "hash": self.block_header.hash,
                "transaction": self.transaction,
            }
        )

    @property
    def to_dict(self):
        block_list = []
        current_block = self
        while current_block:
            block_data = {
                "header": current_block.block_header.to_dict,
                "transaction": current_block.transaction,
            }
            block_list.append(block_data)
            current_block = current_block.previous_block
        return block_list

    @property
    def to_json(self) -> str:
        return json.dumps(self.to_dict)

    def get_transaction(self, transaction: dict) -> dict:
        current_block = self
        while current_block.previous_block:
            if current_block.transaction == transaction:
                return current_block
            current_block = current_block.previous_block
        return {}
