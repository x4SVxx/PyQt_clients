import websockets
import asyncio
import json
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

"""Загрузка config из JSON файла"""
with open('anchors.json') as anchors:
    anchors_config = json.load(anchors)

"""Загрузка rf_config из JSON файла"""
with open('rf_params.json') as rf_params:
    rf_config = json.load(rf_params)

command = ""


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.apikey = ""

        self.setGeometry(400, 300, 700, 600)
        self.setWindowTitle("Websocket_client")

        self.button_node_set_config = QtWidgets.QPushButton(self)
        self.button_node_set_config.setText("SetConfig")
        self.button_node_set_config.move(100, 200)
        self.button_node_set_config.adjustSize()
        self.button_node_set_config.clicked.connect(lambda: self.node_set_config())

    def node_set_config(self):
        global command
        command = "SetConfig 1"


class Client:

    def __init__(self, login, password, server_ip, server_port):
        self.server_ip = server_ip       # ip-адрес сервера
        self.server_port = server_port   # порт сервера
        self.login = login               # логин клиента
        self.password = password         # пароль клиента
        self.apikey = ""                 # apikey - ключ безопасности для общения с сервером
        self.command = ""                # команда для выполнения(вводится из консоли)

    """Функция обработки клиента"""
    async def client_handler(self):
        url = f"ws://{self.server_ip}:{self.server_port}" # url-адрес сервера
        async with websockets.connect(url, ping_interval=None) as ws: # подключение к серверу
            print("CLIENT CONNECTED TO SERVER: " + str(self.server_ip) + ":" + str(self.server_port))
            await ws.send(json.dumps({"action": "Login_client", "login": self.login, "password": self.password})) # отправка сообщения авторизации на сервер
            await asyncio.gather(self.command_handler(ws), self.client_receive(ws)) # запуск асинхронной работы приемной и передающей функций сервера

    """Функция обработки консольных команд клиента"""
    async def command_handler(self, ws):
        while True: # бесконечный цикл для непрерывной проверки ввода команды

            if command.split()[0] == "SetConfig":  # команада установки config
                await ws.send((json.dumps({"action": "SetConfig", "roomid": command.split()[1], "status": "true", "apikey": self.apikey, "data": anchors_config}))) # отправка сообщения с config на сервер

            elif command.split()[0] == "SetRfConfig":  # команада установки rf_config
                await ws.send((json.dumps({"action": "SetRfConfig", "roomid": command.split()[1], "status": "true", "apikey": self.apikey, "data": rf_config}))) # отправка сообщения с rf_config на сервер

            elif command.split()[0] == "Start":  # команада старт
                await ws.send((json.dumps({"action": "Start", "roomid": command.split()[1], "status": "true", "apikey": self.apikey}))) # отправка сообщения с командой start на сервер

            elif command.split()[0] == "Stop":  # команада стоп
                await ws.send((json.dumps({"action": "Stop", "roomid": command.split()[1], "status": "true", "apikey": self.apikey}))) # отправка сообщения с командой stop на сервер


    """Функция приема клиента"""
    async def client_receive(self, ws):
        while True: # запуск бесконечного цикла для непрерывной работы функции
            message = json.loads(await ws.recv()) # прием сообщения от сервера
            print("MESSAGE FROM SERVER: " + str(message))

            if message["status"] == "false": # если статус false - пачать предупреждающего сообдения
                print("---WARNING--- " + str(message["data"]) + " ---WARNING---")

            elif message["action"] == "Login" and message["status"] == "true": # обработка авторизации
                await self.login_on_the_server(message)

    """Функция приема аторизации на сервере"""
    async  def login_on_the_server(self, message):
        self.apikey = message["data"]["apikey"] # apikey - ключ безопасности для общения с сервером
        print("APIKEY: " + self.apikey)

async def qt():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()

if __name__ == '__main__':
    client_login = "TestOrg"          # логин клиента
    client_password = "TestOrgPass"   # пароль клиента
    client_server_ip = "127.0.0.1"    # ip-адрес сервера
    client_server_port = "9000"       # порт сервера
    client = Client(client_login, client_password, client_server_ip, client_server_port) # экземпляр класса клиента
    loop = asyncio.get_event_loop() # асинхронная петля
    loop.create_task(client.client_handler())
    loop.create_task(qt)
    loop.run_forever()