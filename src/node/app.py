import os
from flask import Flask, request

app = Flask(__name__)

PUBLIC_KEY = os.getenv("PUBLIC_KEY")


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/add", methods=["POST"])
def receive_data():
    print(request.json)
    print(PUBLIC_KEY)
    return ("OK", 200)


if __name__ == "__main__":
    app.run()
