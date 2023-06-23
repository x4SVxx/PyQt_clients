import websockets
import asyncio
import json


class Client:

    def __init__(self, login, password, server_ip, server_port):
        self.server_ip = server_ip       # ip-адрес сервера
        self.server_port = server_port   # порт сервера
        self.login = login               # логин клиента
        self.password = password         # пароль клиента
        self.apikey = ""                 # apikey - ключ безопасности для общения с сервером

        self.roomid = "1"                # ID комнаты, в которой установлена нода

    """Функция обработки клиента"""
    async def client_handler(self, command, log_list, anchors_config, rf_config):
        url = f"ws://{self.server_ip}:{self.server_port}" # url-адрес сервера
        async with websockets.connect(url, ping_interval=None) as ws: # подключение к серверу
            print("CLIENT CONNECTED TO SERVER: " + str(self.server_ip) + ":" + str(self.server_port))
            await ws.send(json.dumps({"action": "Login_client", "status": "true", "login": self.login, "password": self.password})) # отправка сообщения авторизации на сервер
            await asyncio.gather(self.client_receive(ws, log_list), self.command_handler(ws, command, anchors_config, rf_config)) # запуск асинхронной работы приемной и передающей функций пользователя

    """Функция обработки команд клиента"""
    async def command_handler(self, ws, command, anchors_config, rf_config):
        while True: # бесконечный цикл для непрерывной проверки ввода команды
            if command.value == "SetConfig":  # команда установки config
                await ws.send((json.dumps({"action": "SetConfig", "roomid": self.roomid, "status": "true", "apikey": self.apikey, "data": anchors_config}))) # отправка сообщения с config на сервер

            elif command.value == "SetRfConfig":  # команда установки rf_config
                await ws.send((json.dumps({"action": "SetRfConfig", "roomid": self.roomid, "status": "true", "apikey": self.apikey, "data": rf_config}))) # отправка сообщения с rf_config на сервер

            elif command.value == "Start":  # команда старт
                await ws.send((json.dumps({"action": "Start", "roomid": self.roomid, "status": "true", "apikey": self.apikey}))) # отправка сообщения с командой start на сервер

            elif command.value == "Stop":  # команда стоп
                await ws.send((json.dumps({"action": "Stop", "roomid": self.roomid, "status": "true", "apikey": self.apikey}))) # отправка сообщения с командой stop на сервер

            command.value = ""
            await asyncio.sleep(0.01)

    """Функция приема клиента"""
    async def client_receive(self, ws, log_list):
        while True: # запуск бесконечного цикла для непрерывной работы функции
            message = json.loads(await ws.recv()) # прием сообщения от сервера
            print("MESSAGE FROM SERVER: " + str(message))

            if "status" in message:
                if message["status"] == "false": # если статус false - печать предупреждающего сообщения
                    print("---WARNING--- " + str(message["data"]) + " ---WARNING---")

            if "action" in message:
                if message["action"] == "Login" and message["status"] == "true": # обработка авторизации
                    await self.login_on_the_server(message)

                elif message["action"] == "Log" and message["status"] == "true": # обработка авторизации
                    log_list.append(message["data"]) # добавление лога в массив мультипроцессорного менеджера

    """Функция приема авторизации на сервере"""
    async  def login_on_the_server(self, message):
        self.apikey = message["data"]["apikey"] # apikey - ключ безопасности для общения с сервером
        print("APIKEY: " + self.apikey)