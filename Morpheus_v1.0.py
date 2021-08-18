import socket
import select
import errno
import threading
import time

from time import sleep

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal

class MyThread(QThread):

    append_message_browser = pyqtSignal(str)

    def run(self):
        HEADER_LENGTH = 10

        IP = "172.16.33.120"
        PORT = 3500
        my_username = ui.username.decode('utf-8')

        # Create a socket
        # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
        # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to a given ip and port
        client_socket.connect((IP, PORT))

        # Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
        client_socket.setblocking(False)

        # Prepare username and header and send them
        # We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
        username = my_username.encode('utf-8')
        username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(username_header + username)

        while True:

            try:
                # Now we want to loop over received messages (there might be more than one) and print them
                while True:

                    # Receive our "header" containing username length, it's size is defined and constant
                    username_header = client_socket.recv(HEADER_LENGTH)

                    # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
                    if not len(username_header):
                        print('Connection closed by the server')
                        sys.exit()

                    # Convert header to int value
                    username_length = int(username_header.decode('utf-8').strip())

                    # Receive and decode username
                    username = client_socket.recv(username_length).decode('utf-8')

                    # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
                    message_header = client_socket.recv(HEADER_LENGTH)
                    message_length = int(message_header.decode('utf-8').strip())
                    message = client_socket.recv(message_length).decode('utf-8')

                    # Print message
                    print(f'{username} > {message}')
                    self.append_message_browser.emit(f'{username} > {message}')

            except IOError as e:
            
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))
                    sys.exit()

                # We just did not receive anything
                continue

            except Exception as e:
                # Any other exception - something happened, exit
                print('Reading error: '.format(str(e)))
                sys.exit()
            


class Ui_Morpheus(object):
    def setupUi(self, Morpheus):
        self.username = ''

        Morpheus.setObjectName("Morpheus")
        Morpheus.resize(441, 727)
        self.centralwidget = QtWidgets.QWidget(Morpheus)
        self.centralwidget.setObjectName("centralwidget")
        self.login_button = QtWidgets.QPushButton(self.centralwidget)
        self.login_button.setGeometry(QtCore.QRect(268, 64, 141, 51))
        self.login_button.setObjectName("login_button")
        self.username_input = QtWidgets.QLineEdit(self.centralwidget)
        self.username_input.setGeometry(QtCore.QRect(20, 70, 221, 41))
        self.username_input.setObjectName("username_input")
        self.message_browser = QtWidgets.QTextBrowser(self.centralwidget)
        self.message_browser.setGeometry(QtCore.QRect(20, 150, 391, 461))
        self.message_browser.setObjectName("message_browser")
        self.send_button = QtWidgets.QPushButton(self.centralwidget)
        self.send_button.setGeometry(QtCore.QRect(310, 630, 91, 41))
        self.send_button.setObjectName("send_button")
        self.send_button.hide()
        self.message_input = QtWidgets.QLineEdit(self.centralwidget)
        self.message_input.setGeometry(QtCore.QRect(20, 630, 281, 41))
        self.message_input.setObjectName("message_input")
        self.message_input.hide()
        Morpheus.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Morpheus)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 441, 20))
        self.menubar.setObjectName("menubar")
        Morpheus.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Morpheus)
        self.statusbar.setObjectName("statusbar")
        Morpheus.setStatusBar(self.statusbar)

        self.retranslateUi(Morpheus)
        self.login_button.clicked.connect(self.login)
        self.send_button.clicked.connect(self.send_message)
        QtCore.QMetaObject.connectSlotsByName(Morpheus)

    def retranslateUi(self, Morpheus):
        _translate = QtCore.QCoreApplication.translate
        Morpheus.setWindowTitle(_translate("Morpheus", "Morpheus"))
        self.login_button.setText(_translate("Morpheus", "Login"))
        self.send_button.setText(_translate("Morpheus", "Send"))

    def send_message(self):
        message = self.message_input.text()
        if message != '':


            self.message = message.encode('utf-8')
            message_header = f"{len(self.message):<{self.HEADER_LENGTH}}".encode('utf-8')
            self.client_socket.send(message_header + self.message)
            # self.message_browser.append(self.username.decode('utf-8') +": "+ self.message.decode('utf-8'))
            self.message_input.clear()


    def login(self):
        print('cheching for login...')
        username = self.username_input.text()
        print(username)
        if len(username) > 0:
            # TODO add username textbot 

            # connect to server with username
            print('Login successful')
            self.username = username.encode('utf-8')
            username_header = f"{len(self.username):<{self.HEADER_LENGTH}}".encode('utf-8')
            self.client_socket.send(username_header + self.username)

            # setup UI
            self.start_apending()
            self.username_input.deleteLater()
            self.login_button.deleteLater()
            self.send_button.show()
            self.message_input.show()

        else:
            print('Login failed')

    def connect(self):
        self.HEADER_LENGTH = 10

        IP = "172.16.33.120"
        PORT = 3500
        # Create a socket
        # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
        # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to a given ip and port
        self.client_socket.connect((IP, PORT))

        # Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
        self.client_socket.setblocking(False)

    def start_apending(self):
        self.thread = MyThread()
        self.thread.append_message_browser.connect(self.apend_message)
        self.thread.start()

    def apend_message(self,others_message):
        self.message_browser.append(others_message)
        
        


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Morpheus = QtWidgets.QMainWindow()
    ui = Ui_Morpheus()
    ui.setupUi(Morpheus)
    ui.connect()
    Morpheus.show()
    sys.exit(app.exec_())

