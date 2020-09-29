import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QFont, QPainter, QColor
from Bot import Bot 
import datetime
from time import localtime, strftime, gmtime
from PyQt5.Qt import *

import os.path

class Ui_MainWindow(object):
    def setupUi(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.resize(367, 472)
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.TextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.TextEdit.setObjectName("TextEdit")
        self.verticalLayout.addWidget(self.TextEdit)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        main_window.setCentralWidget(self.centralwidget)
        self.setWindowIcon(QIcon('icon.jpg')) 

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)



    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "Бот"))
        self.TextEdit.setPlaceholderText(_translate("MainWindow", "Начните беседу ..."))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Введите ваше сообщение..."))
        self.pushButton.setText(_translate("MainWindow", "Отправить сообщение"))




class ChatWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    message_sended = QtCore.pyqtSignal()
    __message = None


    def __init__(self, bot=Bot()):
        super().__init__()
        self.bot = bot
        self.setupUi(self)
        self.center()
        self.__name = ""
        is_ok_pressed = True
        while self.__name == "" and is_ok_pressed == True: #Нельзя ввести пустое имя
            self.__name, is_ok_pressed = self.showDialog()
  
        if is_ok_pressed == False: # Cancel pressed
            self.close()
            self.destroy()
            sys.exit(0)

        self.bot.set_user_name(self.__name)
        self.TextEdit.setReadOnly(True)
        self.lineEdit.setFocus()




        # self.read_history()
        if os.path.exists('textEdit_toHtml.html'): #загружаем историю сообщений из файла
            self.fromHtml()
            # self.TextEdit.setAlignment(Qt.AlignLeft)
        self.init_handlers()



    def init_handlers(self):
        # подключение клик-сигнал к слоту send_message
        self.lineEdit.returnPressed.connect(self.send_message)
        self.pushButton.clicked.connect(self.send_message)
        self.message_sended.connect(self.print_answer)




    def send_message(self):
        try:
            self.__message = self.lineEdit.text()
            if len(self.__message) > 0:
                self.lineEdit.setText('')
                time = strftime("%Y-%m-%d %H:%M:%S", localtime())
                font = QtGui.QFont("Helvetica", 12)
                self.TextEdit.setCurrentFont(font)
                self.TextEdit.append(self.__name + ': ' + self.__message)
                self.TextEdit.moveCursor(QTextCursor.End)
                self.TextEdit.setAlignment(Qt.AlignLeft)

                font = QtGui.QFont("Arial", 8, QtGui.QFont.Light)
                self.TextEdit.setCurrentFont(font)
                self.TextEdit.append(time)
                self.TextEdit.setAlignment(Qt.AlignRight)
                self.toHtml() #пишем историю сообщений в файл

                self.message_sended.emit()
            else:
                self.TextEdit.append('Вы пытаетесь отправить пустое сообщение')
        except:
            self.TextEdit.append('Can\'t send the message')

    # def write_history(self):
    #     text = self.TextEdit.toPlainText()
    #     with open('history.txt', 'w') as file:
    #         file.write(text)
    # def read_history(self):
    #     try:
    #         f = open("history.txt")
    #         mytext = f.read()
    #     except IOError:
    #         print ("No file")
    #     self.TextEdit.setPlainText(mytext)         


    def toHtml(self):
        with open('textEdit_toHtml.html', 'w')as f:
            f.write(self.TextEdit.toHtml())

    def fromHtml(self):
        with open('textEdit_toHtml.html', 'r')as f:
            self.TextEdit.setHtml(f.read())



    def print_answer(self):
        answer = self.bot.answer_message(self.__message)
        font = QtGui.QFont("Helvetica", 12)
        self.TextEdit.setCurrentFont(font)
        self.TextEdit.append('Бот: ' + answer)
        self.TextEdit.setAlignment(Qt.AlignLeft)

        time = strftime("%Y-%m-%d %H:%M:%S", localtime())
        font = QtGui.QFont("Arial", 8, QtGui.QFont.Light)
        self.TextEdit.setCurrentFont(font)
        self.TextEdit.append(time)
        self.TextEdit.setAlignment(Qt.AlignRight)


    def center(self): # центрирование окна на экране
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



    def showDialog(self):
        name, ok = QInputDialog.getText(self, 'Окно авторизации',
            'Введите ваше имя:')
        if ok == False:
            self.close()
            self.destroy() 
        return name, ok


style = '''
QWidget {
    background-color: #333333;
    color: white;
} 
     
QTextEdit {
    background-color:#202020;
    color: white;
}
QLineEdit {
    background-color:#202020;
    color: white;}
QPushButton {
    background-color: #3a4055;
    border-style: outset;
    border-width: 2px;
    border-radius: 10px;
    border-color: #333333;
    font: 15px;
    min-width: 10em;
    padding: 6px;
}

'''





if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(style)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec_())
