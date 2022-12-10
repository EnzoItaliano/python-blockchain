import os
import json

from flask import Flask, request

from .node import Node

PUBLIC_KEY = os.getenv("PUBLIC_KEY")

app = Flask(__name__)


# @app.route("/create_wallet", methods=["POST"])
# def create_node():
#     wallet = Node.create_wallet()

#     response = app.response_class(
#         response=json.dumps(wallet), status=201, mimetype="application/json"
#     )
#     return response


@app.route("/add", methods=["POST"])
def receive_data():
    signature = request.json["signature"]
    transaction_data = request.json["transactionn_data"]
    Node.validate_signature(PUBLIC_KEY, signature, transaction_data)
    return ("OK", 200)


if __name__ == "__main__":
    app.run()
