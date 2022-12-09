import json

from flask import Flask, request

from config import PUBLIC_KEY
from src.node.node import Node

app = Flask(__name__)


@app.route("/create_wallet", methods=["POST"])
def create_node():
    wallet = Node.create_wallet()

    response = app.response_class(
        response=json.dumps(wallet), status=201, mimetype="application/json"
    )
    return response


@app.route("/add", methods=["POST"])
def receive_data():
    print(request.json)
    print(PUBLIC_KEY)
    return ("OK", 200)


if __name__ == "__main__":
    app.run()
