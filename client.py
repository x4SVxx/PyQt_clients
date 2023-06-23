import multiprocessing as mp
import websockets
import asyncio
import json
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


"""Загрузка config из JSON файла"""
with open('anchors.json') as anchors:
    anchors_config = json.load(anchors)

"""Загрузка rf_config из JSON файла"""
with open('rf_params.json') as rf_params:
    rf_config = json.load(rf_params)


apikey = ""
command_flag = False

class Consumer(QThread):
    poped = pyqtSignal(dict)

    def __init__(self, q):
        super().__init__()
        self.q = q

    def run(self):
        while True:
            if not self.q.empty():
                data = q.get()
                self.poped.emit(data)


"""Функция обработки клиента"""
async def client_handler(queue):
    login = "TestOrg"  # логин клиента
    password = "TestOrgPass"  # пароль клиента
    server_ip = "127.0.0.1"  # ip-адрес сервера
    server_port = "9000"  # порт сервера
    url = f"ws://{server_ip}:{server_port}"  # url-адрес сервера
    async with websockets.connect(url, ping_interval=None) as ws:  # подключение к серверу
        print("CLIENT CONNECTED TO SERVER: " + str(server_ip) + ":" + str(server_port))
        await ws.send(json.dumps({"action": "Login_client", "login": login, "password": password}))  # отправка сообщения авторизации на сервер
        # await asyncio.gather(client_receive(ws), command_handler(ws, queue))  # запуск асинхронной работы приемной и передающей функций сервера

        while True:
            queue.put(json.loads(await ws.recv()))
            await command_handler(ws, q)

"""Функция команд клиента"""
async def command_handler(ws, q):
    global command_flag
    global apikey
    while True:
        command_flag = q.get()
        print(command_flag)
        if command_flag:
            command = q.get()
            print(command)

            if command.split()[0] == "SetConfig":  # команада установки config
                await ws.send((json.dumps({"action": "SetConfig", "roomid": command.split()[1], "status": "true", "apikey": apikey, "data": anchors_config}))) # отправка сообщения с config на сервер

            elif command.split()[0] == "SetRfConfig":  # команада установки rf_config
                await ws.send((json.dumps({"action": "SetRfConfig", "roomid": command.split()[1], "status": "true", "apikey": apikey, "data": rf_config}))) # отправка сообщения с rf_config на сервер
                print(ws)
            elif command.split()[0] == "Start":  # команада старт
                await ws.send((json.dumps({"action": "Start", "roomid": command.split()[1], "status": "true", "apikey": apikey}))) # отправка сообщения с командой start на сервер

            elif command.split()[0] == "Stop":  # команада стоп
                await ws.send((json.dumps({"action": "Stop", "roomid": command.split()[1], "status": "true", "apikey": apikey}))) # отправка сообщения с командой stop на сервер

            else: # если ни одно условие не выполняется - сообщение о несуществующей команде
                print("UNKNOWN COMMAND")

            command_flag = False

"""Функция приема клиента"""
async def client_receive(ws):
    while True: # запуск бесконечного цикла для непрерывной работы функции
        message = json.loads(await ws.recv()) # прием сообщения от сервера
        print("MESSAGE FROM SERVER: " + str(message))

        if message["status"] == "false": # если статус false - пачать предупреждающего сообдения
            print("---WARNING--- " + str(message["data"]) + " ---WARNING---")

        elif message["action"] == "Login" and message["status"] == "true": # обработка авторизации
            await login_on_the_server(message)

"""Функция приема аторизации на сервере"""
async  def login_on_the_server(message):
    global apikey
    apikey = message["data"]["apikey"] # apikey - ключ безопасности для общения с сервером
    print("APIKEY: " + apikey)


class Window(QMainWindow):
    def __init__(self, q):
        super().__init__()
        self.setGeometry(400, 300, 700, 600)
        self.setWindowTitle("Websocket_client")

        # thread for data consumer
        self.consumer = Consumer(q)
        self.consumer.poped.connect(self.print_data)
        self.consumer.start()

        self.button_node_set_config = QtWidgets.QPushButton(self)
        self.button_node_set_config.setText("SetConfig")
        self.button_node_set_config.move(100, 100)
        self.button_node_set_config.adjustSize()
        self.button_node_set_config.clicked.connect(node_set_config(q))

        self.button_node_set_rf_config = QtWidgets.QPushButton(self)
        self.button_node_set_rf_config.setText("SetRfConfig")
        self.button_node_set_rf_config.move(100, 200)
        self.button_node_set_rf_config.adjustSize()
        self.button_node_set_rf_config.clicked.connect(node_set_rf_config(q))

        self.button_node_start = QtWidgets.QPushButton(self)
        self.button_node_start.setText("Start")
        self.button_node_start.move(100, 300)
        self.button_node_start.adjustSize()
        self.button_node_start.clicked.connect(node_start(q))

        self.button_node_stop = QtWidgets.QPushButton(self)
        self.button_node_stop.setText("Stop")
        self.button_node_stop.move(100, 400)
        self.button_node_stop.adjustSize()
        self.button_node_stop.clicked.connect(node_stop(q))

    @pyqtSlot(dict)
    def print_data(self, data):
        print(data.get())


def node_set_config(queue):
    global command_flag
    print('NODE_SET_CONFIG')
    command = "SetConfig 1"
    command_flag = True
    queue.put(command_flag)
    queue.put(command)

def node_set_rf_config(queue):
    global command_flag
    print('NODE_SET_RF_CONFIG')
    command = "SetRfConfig 1"
    command_flag = True
    queue.put(command_flag)
    queue.put(command)

def node_start(queue):
    global command_flag
    print('NODE_START')
    command = "Start 1"
    command_flag = True
    queue.put(command_flag)
    queue.put(command)

def node_stop(queue):
    global command_flag
    print('NODE_STOP')
    command = "Stop 1"
    command_flag = True
    queue.put(command_flag)
    queue.put(command)


async def main(q):
    await client_handler(q)


def start_main(q):
    asyncio.run(main(q))


if __name__ == "__main__":
    q = mp.Queue()
    p = mp.Process(name="main", target=start_main, args=(q,), daemon=True)
    p.start()

    app = QApplication(sys.argv)
    window = Window(q)
    window.show()
    app.exec_()
