import multiprocessing
import websocket
import asyncio
import json
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow


"""Загрузка config из JSON файла"""
with open('anchors.json') as anchors:
    anchors_config = json.load(anchors)

"""Загрузка rf_config из JSON файла"""
with open('rf_params.json') as rf_params:
    rf_config = json.load(rf_params)


class Window(QMainWindow):
    def __init__(self, ws):
        super(Window, self).__init__()

        self.apikey = ""

        self.setGeometry(400, 300, 700, 600)
        self.setWindowTitle("Websocket_client")

        self.button_node_connect = QtWidgets.QPushButton(self)
        self.button_node_connect.setText("CONNECT")
        self.button_node_connect.move(100, 100)
        self.button_node_connect.adjustSize()
        self.button_node_connect.clicked.connect(lambda: self.connectweb(ws))

        self.button_node_set_config = QtWidgets.QPushButton(self)
        self.button_node_set_config.setText("SetConfig")
        self.button_node_set_config.move(100, 200)
        self.button_node_set_config.adjustSize()
        self.button_node_set_config.clicked.connect(lambda: self.node_set_config(ws))

        self.button_node_set_rf_config = QtWidgets.QPushButton(self)
        self.button_node_set_rf_config.setText("SetRfConfig")
        self.button_node_set_rf_config.move(100, 300)
        self.button_node_set_rf_config.adjustSize()
        self.button_node_set_rf_config.clicked.connect(lambda: self.node_set_rf_config(ws))

        self.button_node_start = QtWidgets.QPushButton(self)
        self.button_node_start.setText("Start")
        self.button_node_start.move(100, 400)
        self.button_node_start.adjustSize()
        self.button_node_start.clicked.connect(lambda: self.node_start(ws))

        self.button_node_stop = QtWidgets.QPushButton(self)
        self.button_node_stop.setText("Stop")
        self.button_node_stop.move(100, 500)
        self.button_node_stop.adjustSize()
        self.button_node_stop.clicked.connect(lambda: self.node_stop(ws))

    def connectweb(self, ws):
        login = "TestOrg"  # логин клиента
        password = "TestOrgPass"  # пароль клиента
        ws.send(json.dumps({"action": "Login_client", "login": login, "password": password}))
        message = json.loads(ws.recv())
        print(message)
        self.apikey = message["data"]["apikey"]
        print("APIKEY: {0}".format(self.apikey))


    def node_set_config(self, ws):
        ws.send((json.dumps({"action": "SetConfig", "roomid": "1", "status": "true", "apikey": self.apikey, "data": anchors_config})))  # отправка сообщения с config на сервер
        message = json.loads(ws.recv())
        print(message)

    def node_set_rf_config(self, ws):
        ws.send((json.dumps({"action": "SetRfConfig", "roomid": "1", "status": "true", "apikey": self.apikey, "data": rf_config})))  # отправка сообщения с rf_config на сервер
        message = json.loads(ws.recv())
        print(message)

    def node_start(self, ws):
        ws.send((json.dumps({"action": "Start", "roomid": "1", "status": "true", "apikey": self.apikey})))  # отправка сообщения с командой start на сервер
        message = json.loads(ws.recv())
        print(message)


    def node_stop(self, ws):
        ws.send((json.dumps({"action": "Stop", "roomid": "1", "status": "true", "apikey": self.apikey})))  # отправка сообщения с командой stop на сервер
        message = json.loads(ws.recv())
        print(message)

# async def command_handler(ws, queue):
#     while True:
#         if not queue.empty():
#             print('+')
#             command = queue.get()
#             if command == "Connect":
#                 connect_server(ws)


# def connect_server(ws):
#     login = "TestOrg"  # логин клиента
#     password = "TestOrgPass"  # пароль клиента
#     ws.send(json.dumps({"action": "Login_client", "login": login, "password": password}))

def start_pyqt(ws):
    app = QApplication(sys.argv)
    window = Window(ws)
    window.show()
    app.exec_()

# def on_message(ws, message):
#     print(json.loads(message))
#
# async def main(ws, queue):
#     await command_handler(ws, queue)
#
# def on_open(ws, queue):
#     asyncio.run(main(ws, queue))
#
# async def client_receive(ws):
#     while True:
#         print(json.loads(await ws.recv()))
#
# async def main2(ws):
#     await asyncio.gather(client_receive(ws))
#
# def on_open2(ws):
#     asyncio.run(main2(ws))

if __name__ == "__main__":
    # queue = multiprocessing.Queue()
    # pyqt_process = multiprocessing.Process(name="main", target=start_pyqt, args=(queue,), daemon=True)
    # pyqt_process.start()

    # websocket.enableTrace(False)
    ws = websocket.create_connection(f"ws://127.0.0.1:9000")

    start_pyqt(ws)
    # on_open2(ws)

    # ws = websocket.WebSocketApp(f"ws://127.0.0.1:9000", on_message=on_message)
    # ws.on_open = on_open(ws, queue)
    # ws.run_forever()




