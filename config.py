import os

from dotenv import load_dotenv


load_dotenv()

PUBLIC_KEY = bytes(os.getenv("PUBLIC_KEY"), "utf-8")
MY_PORT = int(os.getenv("MY_PORT"))
MY_HOSTNAME = f"{os.getenv('MY_HOSTNAME')}:{MY_PORT}"
MEMPOOL_DIR = os.getenv("MEMPOOL_DIR")
KNOWN_NODES_DIR = os.getenv("KNOWN_NODES_DIR")
BLOCKCHAIN_DIR = os.getenv("BLOCKCHAIN_DIR")
APP_MODE = os.getenv("APP_MODE")
