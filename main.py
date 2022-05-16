import os
import shutil
import sys
import asyncio
import signal
from flask import Flask
from flask import g
from threading import Thread

from tor import Tor
from web import Web

def command_loop(web_obj: Web):
    while True:
        c = input("Enter command ('help' for a list of commands)\n")
        if c == 'q':
            raise KeyboardInterrupt
        elif c == 'u':
            msg = input("Enter message: ")
            web_obj.set_msg(msg)
        elif c == "help":
            print("Commands:\n---'q' to quit\n---'u' to update message that is being shared")


def main():
    tor = Tor()
    tor.connect()
    tor.create_hidden_service()
    try:
        web = Web()
        t = Thread(target=web.run, daemon=True)
        t.start()
        command_loop(web)
    except KeyboardInterrupt:
        return
    finally:
        tor.remove_hidden_service()

if __name__ == "__main__":
    main()