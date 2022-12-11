import json

from flask import Flask, jsonify, request

from src.common.io_blockchain import BlockchainMemory
from src.common.io_mem_pool import MemPool
from src.initialize_blockchain import blockchain
from src.node.transaction_validation.transaction_validation import Transaction


app = Flask(__name__)

mempool = MemPool()
blockchain_memory = BlockchainMemory()

blockchain_base = blockchain()


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
        new_block = NewBlock(blockchain_base)
        new_block.receive(new_block=content["block"])
        new_block.validate()
        new_block.add()
    except (NewBlockException, TransactionException) as new_block_exception:
        return f"{new_block_exception}", 400
    return "Transaction success", 200


@app.route("/add", methods=["POST"])
def receive_data():
    content = request.json
    try:
        transaction = Transaction(blockchain_base)
        transaction.receive(content)
        if transaction.is_new:
            transaction.validate()
            transaction.store()
            transaction.broadcast()
            print("Valid signature")

    except Exception as e:
        return str(e), 400

    return "OK", 200


@app.route("/block", methods=["GET"])
def get_blocks():
    blockchain_base = blockchain_memory.get_blockchain_from_memory()
    return jsonify(blockchain_base.to_dict)


@app.route("/transactions/<transaction_hash>", methods=["GET"])
def get_transaction(transaction_hash):
    blockchain_base = blockchain_memory.get_blockchain_from_memory()
    return jsonify(blockchain_base.get_transaction(transaction_hash))


if __name__ == "__main__":
    app.run()
