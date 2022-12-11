import json
import os


class MemPool:
    def __init__(self):
        self.file_name = os.getenv("MEMPOOL_DIR")

    def get_transactions_from_memory(self):
        with open(self.file_name, "rb") as file_obj:
            current_mem_pool_str = file_obj.read()
            if len(current_mem_pool_str):
                current_mem_pool_list = json.loads(current_mem_pool_str)
            else:
                current_mem_pool_list = []
        return current_mem_pool_list

    def get_first_transaction_from_memory(self):
        with open(self.file_name, "rb") as file_obj:
            current_mem_pool_str = file_obj.read()
            if len(current_mem_pool_str):
                current_mem_pool_list = json.loads(current_mem_pool_str)
            else:
                current_mem_pool_list = []
        return current_mem_pool_list[0]

    def store_transaction_in_memory(self, transactions: list):
        text = json.dumps(transactions).encode("utf-8")
        with open(self.file_name, "wb") as file_obj:
            file_obj.write(text)

    def clear_transactions_from_memory(self):
        open(self.file_name, "w").close()

    def clear_first_transaction_from_memory(self):
        transactions = self.get_transactions_from_memory()
        if len(transactions) > 0:
            transactions.pop(0)
            self.store_transaction_in_memory(transactions)
