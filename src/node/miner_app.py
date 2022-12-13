import logging
import time


from config import MY_HOSTNAME
from src.common.io_mem_pool import MemPool
from src.node.new_block_creation.new_block_creation import BlockException, ProofOfWork

logging.basicConfig(level=logging.DEBUG, format=f"%(asctime)s: %(message)s")


def main():
    my_hostname = MY_HOSTNAME
    mempool = MemPool()
    mempool.clear_transactions_from_memory()

    while True:
        pow = ProofOfWork(my_hostname)
        try:
            pow.create_new_block()
            pow.broadcast()
            mempool.clear_transactions_from_memory()
        except BlockException:
            logging.info("No transaction in mem pool")
        time.sleep(5)


if __name__ == "__main__":
    main()
