from src.common.block import Block, BlockHeader
from src.common.io_blockchain import BlockchainMemory
from src.common.values import NUMBER_OF_LEADING_ZEROS
from src.node.transaction_validation.transaction_validation import Transaction


class NewBlockException(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class NewBlock:
    def __init__(self, blockchain: Block):
        self.blockchain = blockchain
        self.new_block = None
        self.blockchain_memory = BlockchainMemory()

    def receive(self, new_block: dict):
        block_header = BlockHeader(**new_block["header"])
        self.new_block = Block(transaction=new_block["transaction"], block_header=block_header)
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
        transaction = Transaction(self.blockchain)
        transaction.receive(transaction=self.new_block.transaction)
        transaction.validate()

    def add(self):
        self.new_block.previous_block = self.blockchain
        self.blockchain_memory.store_blockchain_in_memory(self.new_block)
