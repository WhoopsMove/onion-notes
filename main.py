import os
import shutil
import sys
from flask import Flask
from flask import g

from tor import Tor

app = Flask(__name__)

message = input("Enter message: ")

@app.route('/')
def index():
    return get_message()

def get_message():
    if 'message' not in g:
        g.message = f"<p>{message}</p>"
    return g.message

def main():
    tor = Tor()
    tor.connect()
    tor.create_hidden_service()
    try:
        app.run()
    except KeyboardInterrupt:
        return
    finally:
        tor.remove_hidden_service()


if __name__ == "__main__":
    main()