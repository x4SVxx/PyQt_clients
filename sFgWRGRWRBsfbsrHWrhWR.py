import multiprocessing
import asyncio
import json
from PyQt5 import QtWidgets
from client_class import  Client
import sys
import PyQt5.QtCore
from PyQt5.Qt import *


"""Загрузка config из JSON файла"""
with open('anchors.json') as anchors:
    anchors_config = json.load(anchors)

"""Загрузка rf_config из JSON файла"""
with open('rf_params.json') as rf_params:
    rf_config = json.load(rf_params)


class Window(QMainWindow):
    def __init__(self, command, log_list):
        super(Window, self).__init__()

        self.left_right_offset = 20 # отступ слева от края окна до начала расположения виджетов
        self.top_bot_offset = 20 # отступ сверху от края окна до начала расположения виджетов
        self.between_widgets_offset = 10 # отступ между виджетов

        self.button_width = 150 # ширина кнопок
        self.button_height = 30 # высота кнопок
        self.button_text_size = 8 # размер текста для кнопок
        self.button_font = "Arial Black" # шрифт текста для кнопок
        self.button_background_color = "#E1E1E1" # цвет кнопок
        self.button_press_background_color = "#7F7F7F" # цвет кнопок при нажатии
        self.button_text_color = "Black" # цвет текста для кнопок
        self.button_border_width = "1" # ширина рамки для кнопок
        self.button_border_color = "Black" # цвет рамки для кнопок
        self.button_border_radius = "5" # радиус закругления краев кнопки

        self.line_edit_width = 150 # ширина поля для ввода
        self.line_edit_height = 30 # высота поля для ввода

        self.label_axes_width = 50 # ширина текстового поля осей
        self.label_axes_height = 12 # высота текстового поля осей
        self.label_axes_font = "Arial" # шрифт текста для текстового поля осей
        self.label_axes_text_size = 10 # размер текста для текстового поля осей

        self.label_input_font = "Arial Black" # шрифт текста для надписи над вводом размера комнаты
        self.label_input_text_size = 7 # размер текста для надписи над вводом размера комнаты
        self.label_input_width = 150 # ширина для надписи над вводом размера комнаты
        self.label_input_height = 15 # высота для надписи над вводом размера комнаты

        self.main_window_geometry()               # функция обработки размеров окна и его положения
        self.creatre_buttons(command, log_list)   # фукнция создания кнопок
        self.create_graphics()                    # функция обработки отрисовки
        self.create_room()                        # функция создания комнаты

    """Функция обработки размеров окна и его положения"""
    def main_window_geometry(self):
        self.SCREEN_WIDTH = QApplication.desktop().width() # разрешение ширины экрана в пикселях
        self.SCREEN_HEIGHT = QApplication.desktop().height() # разрешение высоты экрана в пикселях
        self.window_width = int(self.SCREEN_WIDTH / 10 * 7) # разрешение ширины окна приложения в пикселях (70 % от всей ширины экрана)
        self.window_height = int(self.SCREEN_HEIGHT / 10 * 7) # разрешение высоты окна приложения в пикселях (70 % от всей высоты экрана)
        self.window_x = int(self.SCREEN_WIDTH / 2 - self.window_width / 2) # координата x окна, чтобы окно было открывалось ровно по центру
        self.window_y = int(self.SCREEN_HEIGHT / 2 - self.window_height / 2) # координата y окна, чтобы окно было открывалось ровно по центру

        self.setGeometry(self.window_x, self.window_y, self.window_width, self.window_height) # установка размеров и положения окна
        self.setWindowTitle("Websocket_client") # название окна
        self.setStyleSheet("background-color: #F6F3F3") # цвет окна

    """Функция создания кнопок"""
    def creatre_buttons(self, command, log_list):
        self.button_node_set_config = QtWidgets.QPushButton(self) # объявление кнопки
        self.button_node_set_config.setGeometry(self.left_right_offset, self.top_bot_offset, self.button_width, self.button_height) # положение и размеры
        self.button_node_set_config.setFont(QFont(self.button_font, self.button_text_size)) # шрифт
        self.button_node_set_config.setText("SET CONFIG") # текст
        self.button_node_set_config.setStyleSheet("QPushButton { color: " + self.button_text_color + " }"
                                                  "QPushButton { background-color: " + self.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + self.button_press_background_color + " }"
                                                  "QPushButton { border: " + self.button_border_width + "px solid " + self.button_border_color + " }"
                                                  "QPushButton { border-radius: " + self.button_border_radius + "px }") # стили
        self.button_node_set_config.clicked.connect(lambda: self.set_config(command)) # функция для выполнения

        self.button_node_set_rf_config = QtWidgets.QPushButton(self)
        self.button_node_set_rf_config.setGeometry(self.left_right_offset, self.top_bot_offset + self.button_height + self.between_widgets_offset, self.button_width, self.button_height)
        self.button_node_set_rf_config.setFont(QFont(self.button_font, self.button_text_size))
        self.button_node_set_rf_config.setText("SET RF CONFIG")
        self.button_node_set_rf_config.setStyleSheet("QPushButton { color: " + self.button_text_color + " }"
                                                  "QPushButton { background-color: " + self.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + self.button_press_background_color + " }"
                                                  "QPushButton { border: " + self.button_border_width + "px solid " + self.button_border_color + " }"
                                                  "QPushButton { border-radius: " + self.button_border_radius + "px }")
        self.button_node_set_rf_config.clicked.connect(lambda: self.set_rf_config(command))

        self.button_node_start = QtWidgets.QPushButton(self)
        self.button_node_start.setGeometry(self.left_right_offset, self.top_bot_offset + self.button_height * 2 + self.between_widgets_offset * 2, self.button_width, self.button_height)
        self.button_node_start.setFont(QFont(self.button_font, self.button_text_size))
        self.button_node_start.setText("START")
        self.button_node_start.setStyleSheet("QPushButton { color: " + self.button_text_color + " }"
                                                  "QPushButton { background-color: " + self.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + self.button_press_background_color + " }"
                                                  "QPushButton { border: " + self.button_border_width + "px solid " + self.button_border_color + " }"
                                                  "QPushButton { border-radius: " + self.button_border_radius + "px }")
        self.button_node_start.clicked.connect(lambda: self.set_start(command, log_list))

        self.button_node_stop = QtWidgets.QPushButton(self)
        self.button_node_stop.setGeometry(self.left_right_offset, self.top_bot_offset + self.button_height * 3 + self.between_widgets_offset * 3, self.button_width, self.button_height)
        self.button_node_stop.setFont(QFont(self.button_font, self.button_text_size))
        self.button_node_stop.setText("STOP")
        self.button_node_stop.setStyleSheet("QPushButton { color: " + self.button_text_color + " }"
                                                  "QPushButton { background-color: " + self.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + self.button_press_background_color + " }"
                                                  "QPushButton { border: " + self.button_border_width + "px solid " + self.button_border_color + " }"
                                                  "QPushButton { border-radius: " + self.button_border_radius + "px }")
        self.button_node_stop.clicked.connect(lambda: self.set_stop(command))

        self.button_load_image = QtWidgets.QPushButton(self)
        self.button_load_image.setGeometry(self.left_right_offset, 400, self.button_width, self.button_height)
        self.button_load_image.setFont(QFont(self.button_font, self.button_text_size))
        self.button_load_image.setText("LOAD MAP")
        self.button_load_image.setStyleSheet("QPushButton { color: " + self.button_text_color + " }"
                                                  "QPushButton { background-color: " + self.button_background_color + " }" 
                                                  "QPushButton:pressed { background-color: " + self.button_press_background_color + " }"
                                                  "QPushButton { border: " + self.button_border_width + "px solid " + self.button_border_color + " }"
                                                  "QPushButton { border-radius: " + self.button_border_radius + "px }")
        self.button_load_image.clicked.connect(lambda: self.getFileName())

    """Функция обработки отрисовки"""
    def create_graphics(self):
        self.scene_width = self.window_width - self.left_right_offset * 2 - self.button_width - self.between_widgets_offset * 2 - self.label_axes_width # ширина полотна для отрисовки
        self.scene_height = self.window_height - self.top_bot_offset * 2 - self.label_axes_height # высота полотна для отрисовки

        self.pen = QPen() # ручка
        self.pen.setWidth(3) # ширина ручки

        self.scene = QGraphicsScene() # полотно для отрисовки

        self.graphicView = QGraphicsView(self.scene, self) # выделение области для полотна
        self.graphicView.setGeometry(self.left_right_offset + self.button_width + self.between_widgets_offset * 2 + self.label_axes_width, self.top_bot_offset, self.scene_width, self.scene_height) # размеры области

    """Функция определения размеров комнаты"""
    def create_room(self):
        self.label_x_input = QtWidgets.QLabel(self)
        self.label_x_input.setGeometry(int(self.left_right_offset + self.button_width / 2 - self.label_input_width / 2), self.top_bot_offset + self.button_height * 4 + self.between_widgets_offset * 4, self.label_input_width, self.label_input_height)
        self.label_x_input.setFont(QFont(self.label_input_font, self.label_input_text_size))
        self.label_x_input.setText("SIZE X (METERS)")
        self.label_x_input.setAlignment(Qt.AlignCenter)

        self.label_x_input = QtWidgets.QLabel(self)
        self.label_x_input.setGeometry(int(self.left_right_offset + self.button_width / 2 - self.label_input_width / 2), self.top_bot_offset + self.button_height * 4 + self.between_widgets_offset * 6 + self.label_input_height + self.line_edit_height, self.label_input_width, self.label_input_height)
        self.label_x_input.setFont(QFont(self.label_input_font, self.label_input_text_size))
        self.label_x_input.setText("SIZE Y (METERS)")
        self.label_x_input.setAlignment(Qt.AlignCenter)

        # поля ввода размеров комнаты
        self.LineEdit_size_room_x = QtWidgets.QLineEdit(self)
        self.LineEdit_size_room_x.setGeometry(self.left_right_offset, self.top_bot_offset + self.button_height * 4 + self.between_widgets_offset * 5 + self.label_input_height, self.line_edit_width, self.line_edit_height)

        self.LineEdit_size_room_y = QtWidgets.QLineEdit(self)
        self.LineEdit_size_room_y.setGeometry(self.left_right_offset, self.top_bot_offset + self.button_height * 4 + self.between_widgets_offset * 7 + self.label_input_height * 2 + self.line_edit_height, self.line_edit_width, self.line_edit_height)
        # кнопка отправки размеров комнаты
        self.button_set_room_sizes = QtWidgets.QPushButton(self)
        self.button_set_room_sizes.setGeometry(self.left_right_offset, self.top_bot_offset + self.button_height * 4 + self.between_widgets_offset * 8 + self.label_input_height * 2 + self.line_edit_height * 2, self.button_width, self.button_height)
        self.button_set_room_sizes.setFont(QFont(self.button_font, self.button_text_size))
        self.button_set_room_sizes.setText("SET ROOM SIZES")
        self.button_set_room_sizes.setStyleSheet("QPushButton { color: " + self.button_text_color + " }"
                                                 "QPushButton { background-color: " + self.button_background_color + " }" 
                                                 "QPushButton:pressed { background-color: " + self.button_press_background_color + " }"
                                                 "QPushButton { border: " + self.button_border_width + "px solid " + self.button_border_color + " }"
                                                 "QPushButton { border-radius: " + self.button_border_radius + "px }")
        self.button_set_room_sizes.clicked.connect(lambda: self.set_room_sizes())

        # создание меток для осей
        self.label_0 = QtWidgets.QLabel(self)
        self.label_0.setGeometry(self.left_right_offset + self.between_widgets_offset + self.button_width, self.top_bot_offset + self.scene_height + self.between_widgets_offset, self.label_axes_width, self.label_axes_height)
        self.label_0.setFont(QFont(self.label_axes_font, self.label_axes_text_size))
        self.label_0.setText("")
        self.label_0.setAlignment(Qt.AlignCenter)

        self.label_y1 = QtWidgets.QLabel(self)
        self.label_y1.setGeometry(self.left_right_offset + self.between_widgets_offset + self.button_width, int(self.top_bot_offset + self.scene_height / 10 * 9 - self.label_axes_height / 2), self.label_axes_width, self.label_axes_height)
        self.label_y1.setFont(QFont(self.label_axes_font, self.label_axes_text_size))
        self.label_y1.setText("")
        self.label_y1.setAlignment(Qt.AlignCenter)

        self.label_y2 = QtWidgets.QLabel(self)
        self.label_y2.setGeometry(self.left_right_offset + self.between_widgets_offset + self.button_width, int(self.top_bot_offset + self.scene_height / 10 * 8 - self.label_axes_height / 2), self.label_axes_width, self.label_axes_height)
        self.label_y2.setFont(QFont(self.label_axes_font, self.label_axes_text_size))
        self.label_y2.setText("")
        self.label_y2.setAlignment(Qt.AlignCenter)

        self.label_y3 = QtWidgets.QLabel(self)
        self.label_y3.setGeometry(self.left_right_offset + self.between_widgets_offset + self.button_width, int(self.top_bot_offset + self.scene_height / 10 * 7 - self.label_axes_height / 2), self.label_axes_width, self.label_axes_height)
        self.label_y3.setFont(QFont(self.label_axes_font, self.label_axes_text_size))
        self.label_y3.setText("")
        self.label_y3.setAlignment(Qt.AlignCenter)

        self.label_y4 = QtWidgets.QLabel(self)
        self.label_y4.setGeometry(self.left_right_offset + self.between_widgets_offset + self.button_width, int(self.top_bot_offset + self.scene_height / 10 * 6 - self.label_axes_height / 2), self.label_axes_width, self.label_axes_height)
        self.label_y4.setFont(QFont(self.label_axes_font, self.label_axes_text_size))
        self.label_y4.setText("")
        self.label_y4.setAlignment(Qt.AlignCenter)

        self.label_y5 = QtWidgets.QLabel(self)
        self.label_y5.setGeometry(self.left_right_offset + self.between_widgets_offset + self.button_width, int(self.top_bot_offset + self.scene_height / 10 * 5 - self.label_axes_height / 2), self.label_axes_width, self.label_axes_height)
        self.label_y5.setFont(QFont(self.label_axes_font, self.label_axes_text_size))
        self.label_y5.setText("")
        self.label_y5.setAlignment(Qt.AlignCenter)

        self.label_y6 = QtWidgets.QLabel(self)
        self.label_y6.setGeometry(self.left_right_offset + self.between_widgets_offset + self.button_width, int(self.top_bot_offset + self.scene_height / 10 * 4 - self.label_axes_height / 2), self.label_axes_width, self.label_axes_height)
        self.label_y6.setFont(QFont(self.label_axes_font, self.label_axes_text_size))
        self.label_y6.setText("")
        self.label_y6.setAlignment(Qt.AlignCenter)

        self.label_y7 = QtWidgets.QLabel(self)
        self.label_y7.setGeometry(self.left_right_offset + self.between_widgets_offset + self.button_width, int(self.top_bot_offset + self.scene_height / 10 * 3 - self.label_axes_height / 2), self.label_axes_width, self.label_axes_height)
        self.label_y7.setFont(QFont(self.label_axes_font, self.label_axes_text_size))
        self.label_y7.setText("")
        self.label_y7.setAlignment(Qt.AlignCenter)

        self.label_y8 = QtWidgets.QLabel(self)
        self.label_y8.setGeometry(self.left_right_offset + self.between_widgets_offset + self.button_width, int(self.top_bot_offset + self.scene_height / 10 * 2 - self.label_axes_height / 2), self.label_axes_width, self.label_axes_height)
        self.label_y8.setFont(QFont(self.label_axes_font, self.label_axes_text_size))
        self.label_y8.setText("")
        self.label_y8.setAlignment(Qt.AlignCenter)

        self.label_y9 = QtWidgets.QLabel(self)
        self.label_y9.setGeometry(self.left_right_offset + self.between_widgets_offset + self.button_width, int(self.top_bot_offset + self.scene_height / 10 * 1 - self.label_axes_height / 2), self.label_axes_width, self.label_axes_height)
        self.label_y9.setFont(QFont(self.label_axes_font, self.label_axes_text_size))
        self.label_y9.setText("")
        self.label_y9.setAlignment(Qt.AlignCenter)

        self.label_y10 = QtWidgets.QLabel(self)
        self.label_y10.setGeometry(self.left_right_offset + self.between_widgets_offset + self.button_width, int(self.top_bot_offset - self.label_axes_height / 2), self.label_axes_width, self.label_axes_height)
        self.label_y10.setFont(QFont(self.label_axes_font, self.label_axes_text_size))
        self.label_y10.setText("")
        self.label_y10.setAlignment(Qt.AlignCenter)


        self.label_x1 = QtWidgets.QLabel(self)
        self.label_x1.setGeometry(int(self.left_right_offset + self.button_width + self.between_widgets_offset * 2 + self.label_axes_width + self.scene_width / 10 * 1 - self.label_axes_width / 2), int(self.top_bot_offset + self.scene_height + self.between_widgets_offset + self.label_axes_height / 2), self.label_axes_width, self.label_axes_height)
        self.label_x1.setFont(QFont(self.label_axes_font, self.label_axes_text_size))
        self.label_x1.setText("")
        self.label_x1.setAlignment(Qt.AlignCenter)

        self.label_x2 = QtWidgets.QLabel(self)
        self.label_x2.setGeometry(int(self.left_right_offset + self.button_width + self.between_widgets_offset * 2 + self.label_axes_width + self.scene_width / 10 * 2 - self.label_axes_width / 2), int(self.top_bot_offset + self.scene_height + self.between_widgets_offset + self.label_axes_height / 2), self.label_axes_width, self.label_axes_height)
        self.label_x2.setFont(QFont(self.label_axes_font, self.label_axes_text_size))
        self.label_x2.setText("")
        self.label_x2.setAlignment(Qt.AlignCenter)

        self.label_x3 = QtWidgets.QLabel(self)
        self.label_x3.setGeometry(int(self.left_right_offset + self.button_width + self.between_widgets_offset * 2 + self.label_axes_width + self.scene_width / 10 * 3 - self.label_axes_width / 2), int(self.top_bot_offset + self.scene_height + self.between_widgets_offset + self.label_axes_height / 2), self.label_axes_width, self.label_axes_height)
        self.label_x3.setFont(QFont(self.label_axes_font, self.label_axes_text_size))
        self.label_x3.setText("")
        self.label_x3.setAlignment(Qt.AlignCenter)

        self.label_x4 = QtWidgets.QLabel(self)
        self.label_x4.setGeometry(int(self.left_right_offset + self.button_width + self.between_widgets_offset * 2 + self.label_axes_width + self.scene_width / 10 * 4 - self.label_axes_width / 2), int(self.top_bot_offset + self.scene_height + self.between_widgets_offset + self.label_axes_height / 2), self.label_axes_width, self.label_axes_height)
        self.label_x4.setFont(QFont(self.label_axes_font, self.label_axes_text_size))
        self.label_x4.setText("")
        self.label_x4.setAlignment(Qt.AlignCenter)

        self.label_x5 = QtWidgets.QLabel(self)
        self.label_x5.setGeometry(int(self.left_right_offset + self.button_width + self.between_widgets_offset * 2 + self.label_axes_width + self.scene_width / 10 * 5 - self.label_axes_width / 2), int(self.top_bot_offset + self.scene_height + self.between_widgets_offset + self.label_axes_height / 2), self.label_axes_width, self.label_axes_height)
        self.label_x5.setFont(QFont(self.label_axes_font, self.label_axes_text_size))
        self.label_x5.setText("")
        self.label_x5.setAlignment(Qt.AlignCenter)

        self.label_x6 = QtWidgets.QLabel(self)
        self.label_x6.setGeometry(int(self.left_right_offset + self.button_width + self.between_widgets_offset * 2 + self.label_axes_width + self.scene_width / 10 * 6 - self.label_axes_width / 2), int(self.top_bot_offset + self.scene_height + self.between_widgets_offset + self.label_axes_height / 2), self.label_axes_width, self.label_axes_height)
        self.label_x6.setFont(QFont(self.label_axes_font, self.label_axes_text_size))
        self.label_x6.setText("")
        self.label_x6.setAlignment(Qt.AlignCenter)

        self.label_x7 = QtWidgets.QLabel(self)
        self.label_x7.setGeometry(int(self.left_right_offset + self.button_width + self.between_widgets_offset * 2 + self.label_axes_width + self.scene_width / 10 * 7 - self.label_axes_width / 2), int(self.top_bot_offset + self.scene_height + self.between_widgets_offset + self.label_axes_height / 2), self.label_axes_width, self.label_axes_height)
        self.label_x7.setFont(QFont(self.label_axes_font, self.label_axes_text_size))
        self.label_x7.setText("")
        self.label_x7.setAlignment(Qt.AlignCenter)

        self.label_x8 = QtWidgets.QLabel(self)
        self.label_x8.setGeometry(int(self.left_right_offset + self.button_width + self.between_widgets_offset * 2 + self.label_axes_width + self.scene_width / 10 * 8 - self.label_axes_width / 2), int(self.top_bot_offset + self.scene_height + self.between_widgets_offset + self.label_axes_height / 2), self.label_axes_width, self.label_axes_height)
        self.label_x8.setFont(QFont(self.label_axes_font, self.label_axes_text_size))
        self.label_x8.setText("")
        self.label_x8.setAlignment(Qt.AlignCenter)

        self.label_x9 = QtWidgets.QLabel(self)
        self.label_x9.setGeometry(int(self.left_right_offset + self.button_width + self.between_widgets_offset * 2 + self.label_axes_width + self.scene_width / 10 * 9 - self.label_axes_width / 2), int(self.top_bot_offset + self.scene_height + self.between_widgets_offset + self.label_axes_height / 2), self.label_axes_width, self.label_axes_height)
        self.label_x9.setFont(QFont(self.label_axes_font, self.label_axes_text_size))
        self.label_x9.setText("")
        self.label_x9.setAlignment(Qt.AlignCenter)

        self.label_x10 = QtWidgets.QLabel(self)
        self.label_x10.setGeometry(int(self.left_right_offset + self.button_width + self.between_widgets_offset * 2 + self.label_axes_width + self.scene_width / 10 * 10 - self.label_axes_width / 2), int(self.top_bot_offset + self.scene_height + self.between_widgets_offset + self.label_axes_height / 2), self.label_axes_width, self.label_axes_height)
        self.label_x10.setFont(QFont(self.label_axes_font, self.label_axes_text_size))
        self.label_x10.setText("")
        self.label_x10.setAlignment(Qt.AlignCenter)


    """Функция запуска таймера для непрерывной отрисовки меток"""
    def start_draw(self, log_list):
        self.timer = PyQt5.QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.draw(log_list))
        self.timer.start(50)

    """Функция отрисовки меток"""
    def draw(self, log_list):
        self.dot = self.scene.addEllipse(0, 0, 3, 3, self.pen)
        try:
            msg = log_list.pop(0)
            self.dot_x = msg["x"]
            self.dot_y = msg["y"]
            self.dot.setPos(self.dot_x, self.dot_y)
        except:
            print("ERROR IN DRAW")

    """Функции для обработки нажатия кнопок"""
    def set_config(self, command):
        command.value = "SetConfig"

    def set_rf_config(self, command):
        command.value = "SetRfConfig"

    def set_start(self, command, log_list):
        command.value = "Start"
        self.start_draw(log_list)

    def set_stop(self, command):
        command.value = "Stop"

    """Функция установки размеров комнаты"""
    def set_room_sizes(self):
        self.size_room_x = float(self.LineEdit_size_room_x.text()) # ширина комнаты
        self.size_room_y = float(self.LineEdit_size_room_y.text()) # высота (длина)

        self.px_x = self.scene_width / self.size_room_x # пикселей в метре по оси OX
        self.px_y = self.scene_height / self.size_room_y # пикселей в метре по оси OY
        # заполнение размеров комнаты (10 отсечек на каждую ось)
        self.label_0.setText("0")
        self.label_x1.setText(str(round(self.size_room_x / 10 * 1, 2)))
        self.label_x2.setText(str(round(self.size_room_x / 10 * 2, 2)))
        self.label_x3.setText(str(round(self.size_room_x / 10 * 3, 2)))
        self.label_x4.setText(str(round(self.size_room_x / 10 * 4, 2)))
        self.label_x5.setText(str(round(self.size_room_x / 10 * 5, 2)))
        self.label_x6.setText(str(round(self.size_room_x / 10 * 6, 2)))
        self.label_x7.setText(str(round(self.size_room_x / 10 * 7, 2)))
        self.label_x8.setText(str(round(self.size_room_x / 10 * 8, 2)))
        self.label_x9.setText(str(round(self.size_room_x / 10 * 9, 2)))
        self.label_x10.setText(str(round(self.size_room_x / 10 * 10, 2)))

        self.label_y1.setText(str(round(self.size_room_y / 10 * 1, 2)))
        self.label_y2.setText(str(round(self.size_room_y / 10 * 2, 2)))
        self.label_y3.setText(str(round(self.size_room_y / 10 * 3, 2)))
        self.label_y4.setText(str(round(self.size_room_y / 10 * 4, 2)))
        self.label_y5.setText(str(round(self.size_room_y / 10 * 5, 2)))
        self.label_y6.setText(str(round(self.size_room_y / 10 * 6, 2)))
        self.label_y7.setText(str(round(self.size_room_y / 10 * 7, 2)))
        self.label_y8.setText(str(round(self.size_room_y / 10 * 8, 2)))
        self.label_y9.setText(str(round(self.size_room_y / 10 * 9, 2)))
        self.label_y10.setText(str(round(self.size_room_y / 10 * 10, 2)))

    """Функция диалогового окна для загрузки плана комнаты"""
    def getFileName(self):
        filename, filetype = QFileDialog.getOpenFileName(self, "Выбрать файл", ".", "Image Files (*.png *.jpg *.bmp *.jpeg)")
        if filename:
            pic = QGraphicsPixmapItem()
            pic.setPixmap(QPixmap(filename).scaled(self.scene_width - 5, self.scene_height - 5))
            self.scene.addItem(pic)


"""Функция запуска клиента"""
async def client_handler(command, log_list):
    login = "TestOrg"  # логин клиента
    password = "TestOrgPass"  # пароль клиента
    # server_ip = "10.3.168.117"  # ip-адрес сервера
    server_ip = "127.0.0.1"  # ip-адрес сервера
    server_port = "8000"  # порт сервера
    client = Client(login, password, server_ip, server_port)
    loop = asyncio.get_event_loop() # асинхронная петля
    loop.run_until_complete(await client.client_handler(command, log_list, anchors_config, rf_config)) # запуск петли и функции обработки клиента

"""Данная конструкция необходима для асинхронного запуска клиента из неасинхронной функции"""
async def main(command, log_list):
    await client_handler(command, log_list)

def start_main(command, log_list):
    asyncio.run(main(command, log_list))
"""---------------------------------------------------------------------------------------"""

def start_qt(command, log_list):
    app = QApplication(sys.argv)
    window = Window(command, log_list)
    window.show()
    app.exec_()


if __name__ == "__main__":
    manager = multiprocessing.Manager() # менеджер модуля multiprocessing для обмена данными между процессами
    command = manager.Value('command', "") # присваивание переменной менеджера пустой строки
    manager_log = multiprocessing.Manager() # менеджер модуля multiprocessing для обмена данными между процессами
    log_list = manager_log.list() # лист для передачи логов между процессами
    process_1 = multiprocessing.Process(name="start_main", target=start_main, args=(command, log_list,), daemon=True) # создание процесса
    process_1.start() # запуск процесса
    start_qt(command, log_list) # запуск GUI