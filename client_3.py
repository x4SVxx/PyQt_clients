import websocket
import json


def on_message(ws, message):
    print(json.loads(message))


def on_open(ws):
        login = "TestOrg"  # логин клиента
        password = "TestOrgPass"  # пароль клиента
        ws.send(json.dumps({"action": "Login_client", "login": login, "password": password}))


if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(f"ws://127.0.0.1:9000", on_message = on_message)
    ws.on_open = on_open
    ws.run_forever()