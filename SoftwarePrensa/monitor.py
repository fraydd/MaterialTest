from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore

import serial
import serial.tools.list_ports as list_ports

TAGS = {
    'P1F': 'lectura de Fuerza en el Pistón 1',
    'P2F': 'lectura de Fuerza en el Pistón 2',
    'P3F': 'lectura de Fuerza en el Pistón 3'
}


class Monitor(QtWidgets.QMainWindow):
    def __init__(self):
        super(Monitor, self).__init__()

        self.ui = uic.loadUi('window.ui', self)
        self.serial = serial.Serial()
        self.message = ''

        ports = list_ports.comports()

        for baud in self.serial.BAUDRATES:
            self.ui.baudOptions.addItem(str(baud))

        self.ui.baudOptions.setCurrentIndex(self.serial.BAUDRATES.index(9600))

        if ports:
            for port in ports:
                self.ui.portOptions.addItem(port.device)

            self.serial.baudrate = 9600
            self.serial.port = self.ui.portOptions.currentText()
            self.serial.open()
        self.ui.sendButton.clicked.connect(self.send)
        self.timer = QtCore.QTimer()
        if self.serial.is_open:
            self.timer.start(100)
            self.timer.timeout.connect(self.read)

    def send(self):
        data = self.ui.inputEdit.text()
        self.serial.write(data.encode('utf-8'))
        self.ui.inputEdit.setText('')

    def read(self):
        if self.serial.is_open:
            if self.serial.in_waiting > 0:
                data = self.serial.read().decode('utf-8')
                if data == '!':
                    self.recognize()
                    self.message = ''
                    data = ''
                self.message += data

    def recognize(self):
        tag = self.message[0:3]
        value = self.message[3:]
        if tag in TAGS:
            self.ui.textEdit.append('Se obtuvo una ' + TAGS[tag])
            self.ui.textEdit.append('Con el siguiente valor: ' + value)
        else:
            self.ui.textEdit.append('Etiqueta no reconocida')

    def __del__(self):
        if self.serial.is_open:
            self.serial.close()
