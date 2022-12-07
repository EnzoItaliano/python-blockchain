# node/block.py

from datetime import datetime


class Block(object):
    def __init__(self, timestamp: float, transaction_data: str, previous_block=None):
        self.timestamp = timestamp
        self.transaction_data = transaction_data
        self.previous_block = previous_block
