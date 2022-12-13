import json
import logging
import os

from flask import Flask, jsonify, request

from config import APP_MODE, BLOCKCHAIN_DIR, MEMPOOL_DIR, MY_HOSTNAME, MY_PORT
from src.common.io_blockchain import BlockchainMemory
from src.common.io_known_nodes import KnownNodesMemory
from src.common.io_mem_pool import MemPool
from src.common.network import Network
from src.common.node import Node
from src.node.new_block_validation.new_block_validation import NewBlock, NewBlockException
from src.node.transaction_validation.transaction_validation import (
    Transaction,
    TransactionException,
)

app = Flask(__name__)

blockchain_memory = BlockchainMemory()


@app.route("/create_wallet", methods=["POST"])
def create_node():
    wallet = Transaction.create_wallet()

    response = app.response_class(
        response=json.dumps(wallet), status=201, mimetype="application/json"
    )
    return response


@app.route("/block", methods=["POST"])
def validate_block():
    content = request.json
    blockchain_base = blockchain_memory.get_blockchain_from_memory()
    try:
        new_block = NewBlock(blockchain_base, MY_HOSTNAME)
        new_block.receive(new_block=content["block"], sender=content["sender"])
        new_block.validate()
        new_block.add()
        new_block.clear_block_transactions_from_mempool()
        new_block.broadcast()
    except (NewBlockException, TransactionException) as new_block_exception:
        return f"{new_block_exception}", 400
    return "Transaction success", 200


@app.route("/transactions", methods=["POST"])
def receive_data():
    logging.info("New transaction validation request")
    content = request.json
    logging.info(f"Transaction: {content}")
    blockchain_base = blockchain_memory.get_blockchain_from_memory()
    try:
        transaction = Transaction(blockchain_base, MY_HOSTNAME)
        transaction.receive(transaction=content)
        if transaction.is_new:
            transaction.validate()
            transaction.store()
            transaction.broadcast()
    except TransactionException as transaction_exception:
        return f"{transaction_exception}", 400
    return "Transaction success", 200


@app.route("/block", methods=["GET"])
def get_blocks():
    logging.info("Block request")
    blockchain_base = blockchain_memory.get_blockchain_from_memory()
    return jsonify(blockchain_base.to_dict)


@app.route("/transactions/<transaction_hash>", methods=["GET"])
def get_transaction(transaction_hash):
    logging.info("Transaction request")
    blockchain_base = blockchain_memory.get_blockchain_from_memory()
    return jsonify(blockchain_base.get_transaction(json.loads(transaction_hash)))


@app.route("/new_node_advertisement", methods=["POST"])
def new_node_advertisement():
    logging.info("New node advertisement request")
    content = request.json
    hostname = content["hostname"]
    known_nodes_memory = KnownNodesMemory()
    try:
        new_node = Node(hostname)
        known_nodes_memory.store_new_node(new_node)
    except TransactionException as transaction_exception:
        return f"{transaction_exception}", 400
    return "New node advertisement success", 200


@app.route("/known_node_request", methods=["GET"])
def known_node_request():
    logging.info("Known node request")
    return jsonify(network.return_known_nodes())


@app.route("/restart", methods=["POST"])
def restart():
    logging.info("Node restart request")
    my_node = Node(MY_HOSTNAME)
    network = Network(my_node)
    mempool = MemPool()
    mempool.clear_transactions_from_memory()
    network.join_network()
    return "Restart success", 200


def main():
    global network
    open(MEMPOOL_DIR, "w").close() if not os.path.exists(MEMPOOL_DIR) else None
    open(BLOCKCHAIN_DIR, "w").close() if not os.path.exists(BLOCKCHAIN_DIR) else None
    my_node = Node(MY_HOSTNAME)
    network = Network(my_node)
    network.join_network()
    app.run(host=os.getenv("MY_HOSTNAME"), port=MY_PORT)


if __name__ == "__main__":
    main()
