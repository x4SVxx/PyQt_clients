import threading
from ctypes import wstring_at
import json
import time
import websocket
import time
import socket

def on_message(ws, json_message):
    print(json.loads(json_message))


def on_error(ws, error):
    print(error)

def on_close(ws):
    ws.close()

def on_open(ws):
    pass

if __name__ == "__main__":
    websocket.enableTrace(False)
    input = websocket.WebSocketApp("ws://127.0.0.1:8000",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    input.on_open = on_open
    input.run_forever()