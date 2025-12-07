import redis
import os
from dotenv import load_dotenv

load_dotenv()

def conectar_keydb():
    try:
        r = redis.Redis(
            host=os.getenv("KEYDB_HOST"),
            port=int(os.getenv("KEYDB_PORT")),
            password=os.getenv("KEYDB_PASSWORD"),
            decode_responses=True
        )
        r.ping()
        return r
    except redis.ConnectionError:
        print("Error: No se pudo conectar a KeyDB")
        exit()
