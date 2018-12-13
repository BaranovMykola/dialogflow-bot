import os
import pyswip as ps
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import*
import PyQt5.QtCore as qc
from PyQt5 import QtGui


class EnterPressedSignal(QObject):
    pressed = pyqtSignal()


class UserInput(QLineEdit):
    def __init__(self):
        super(QLineEdit, self).__init__()
        self.sgn = EnterPressedSignal()

    def keyPressEvent(self, qKeyEvent):
        super(UserInput, self).keyPressEvent(qKeyEvent)
        if qKeyEvent.key() == qc.Qt.Key_Return:
            self.sgn.pressed.emit()


class BotMessaging:
    def __init__(self, bot):
        self.UserName = "Olya"
        self.bot = bot
        self.app = QApplication([])

        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.app.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'logo.ico'))

        self.window = QWidget()
        self.window.setWindowTitle('Food talk')
        self.layout = QVBoxLayout()
        self.logOutput = QTextEdit()
        self.logOutput.setReadOnly(True)
        self.logOutput.setLineWrapMode(QTextEdit.NoWrap)
        self.layout.addWidget(self.logOutput)
        self.userInputTextEdit = UserInput()
        self.layout.addWidget(self.userInputTextEdit)
        self.userInputTextEdit.sgn.pressed.connect(self.SendButtonClick)
        self.sendButton = QPushButton('Send')
        self.sendButton.clicked.connect(self.SendButtonClick)
        self.layout.addWidget(self.sendButton)
        self.window.setLayout(self.layout)
        self.window.show()
        self.app.exec_()


    def SendButtonClick(self):#use bot here
        userDefault="User: "
        user_says = self.userInputTextEdit.text()
        self.logOutput.append(userDefault+user_says)
        print("USER: "+ user_says)
        self.userInputTextEdit.setText("")
        try:
            bot_answer = self.bot.say(user_says)[0]
            print("Bot: "+bot_answer)
            botDefault = "Bot: "
            self.logOutput.append(botDefault + bot_answer)

            c = self.bot.contexts
            check_dict(c)

            self.prolog_log()

        except:
            print("Bot: We are offline. I can't help you, sorry. Check your internet connection")


    def prolog_log(self):
        try:
            prolog = ps.Prolog()
            prolog.consult("./prolog.pl")
            for i in prolog.query("order(X,Y)"):
                print('{}\torder\t{}'.format(i['X'].upper(), i['Y'].upper()))
        except:

            pass




def check_dict(dict):
    if 'given-name' in dict.keys() and 'foods' in dict.keys():
        write_to_prolog(dict)


def write_to_prolog(dict):
    str = 'order({0},{1}).'.format(dict['given-name'].lower(), dict['foods'].lower())

    with open('prolog.pl', 'r') as pl:
        lines = [x.strip() for x in pl.readlines()]

    with open('prolog.pl', 'a+') as pl:
        # lines = [x.strip() for x in pl.readlines()]
        if str not in lines:
            pl.write('\n'+str)