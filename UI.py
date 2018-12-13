import os
import pyswip as ps
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import*
import PyQt5.QtCore as qc
from PyQt5 import QtGui


class EnterPressedSignal(QObject):
    pressed = pyqtSignal()


class PhraseWidget(QWidget):
    def __init__(self, imgname, label):
        super(PhraseWidget, self).__init__()
        self.current_layout = QHBoxLayout()
        img_label = QLabel()
        img_label.setPixmap(QtGui.QPixmap(imgname))
        self.current_layout.addWidget(img_label)
        self.current_layout.addWidget(label)
        self.setLayout(self.current_layout)


class DynamicScrollableArea(QWidget):
    def __init__(self):
        super(DynamicScrollableArea, self).__init__()
        self.widget = QWidget()
        layout = QVBoxLayout(self)

        layout.addStretch()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.widget)

        scroll.setWidgetResizable(True)
        scroll.setWidget(self.widget)
        self.widget.setLayout(layout)

        vLayout = QVBoxLayout(self)
        vLayout.addWidget(scroll)
        self.setLayout(vLayout)

    def add_new_label(self, text, answertype):#answer type means whether this is user or bot answer
        label = QLabel(text)
        phrase = PhraseWidget(answertype, label)
        layout = self.widget.layout()
        layout.insertWidget(layout.count(), phrase)


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
        self.bot = bot
        self.app = QApplication([])

        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.app.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'logo.ico'))

        self.window = QWidget()
        self.window.setWindowTitle('Food talk')
        self.layout = QVBoxLayout()

        self.conversation = DynamicScrollableArea()
        self.layout.addWidget(self.conversation)

        self.userInputTextEdit = UserInput()
        self.layout.addWidget(self.userInputTextEdit)
        self.userInputTextEdit.sgn.pressed.connect(self.SendButtonClick)

        self.sendButton = QPushButton('Send')
        self.sendButton.clicked.connect(self.SendButtonClick)
        self.layout.addWidget(self.sendButton)
        self.endConversationButton = QPushButton("End conversation")
        self.endConversationButton.clicked.connect(self.EndConvButtonClick)
        self.layout.addWidget(self.endConversationButton)
        self.window.setLayout(self.layout)
        self.window.show()
        self.app.exec_()


    def EndConvButtonClick(self):
        pl_data = self.get_prolog_data()
        text="What people order:\n"
        for k in pl_data:
            text+=k+ " ordered:\n"
            for i in pl_data[k]:
                text+=" - "+i+"\n"

        QMessageBox.about(self.window, "Orders", str(text))
        self.app.closeAllWindows()
        pass


    def SendButtonClick(self):
        user_says = self.userInputTextEdit.text()
        self.conversation.add_new_label(user_says,"user.png")
        print("USER: "+ user_says)
        self.userInputTextEdit.setText("")
        try:
            bot_answer = self.bot.say(user_says)[0]
            print("Bot: "+bot_answer)
            self.conversation.add_new_label(bot_answer, "bot.png")
            c = self.bot.contexts
            check_dict(c)

            self.prolog_log()

        except:
            bot_answer = "We are offline. I can't help you, sorry. Check your internet connection"
            self.conversation.add_new_label(bot_answer, "bot.png")


    def prolog_log(self):
        try:
            prolog = ps.Prolog()
            prolog.consult("./prolog.pl")
            for i in prolog.query("order(X,Y)"):
                print('{}\torder\t{}'.format(i['X'].upper(), i['Y'].upper()))
        except:
            pass


    def get_prolog_data(self):
        data = {}
        try:
            prolog = ps.Prolog()
            prolog.consult("./prolog.pl")
            for i in prolog.query("order(X,Y)"):
               # print(i['X'])
               # print(i['Y'])
                if i['X'] in data:
                    data[i['X']].append(i['Y'])
                else:
                    data[i['X']] = [i['Y']]
            return data
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