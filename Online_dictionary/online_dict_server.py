from socket import *
from multiprocessing import Process
from signal import *
from dict_db import *
import time

# 全局变量
ADDR = ("0.0.0.0", 11111)


class OnlineDict(Process):
    def __init__(self, connfd):
        super().__init__()
        self.connfd = connfd
        self.db = DictTable()
        self.db.cursor()

    def run(self):
        while True:
            data = self.connfd.recv(1024).decode()
            if data[:1] == "R":
                self.register(data)

            elif data[:1] == "F":
                self.find_word(data)
            elif data[:1] == "L":
                self.login(data)
            elif data[:1] == "H":
                self.history(data)
            elif data[:1] == "Q":
                self.connfd.close()
                self.db.close()
                return

    def register(self, data):
        name = data.split(" ")[1]
        password = data.split(" ")[-1]
        if self.db.register(name, password):
            self.connfd.send(b"OK")
        else:
            self.connfd.send(b"FAIL")

    def find_word(self, data):
        name = data.split(" ")[1]
        word = data.split(" ")[-1]
        mean = self.db.find_word(name, word)
        if mean:
            msg = "%s:%s" % (word, mean[0])
            self.connfd.send(msg.encode())
        else:
            self.connfd.send(b"FAIl")

    def history(self, data):
        name = data.split(" ")[1]
        for i in self.db.history(name):
            msg = "%s %s %s\n" % i
            self.connfd.send(msg.encode())
        else:
            time.sleep(0.1)
            self.connfd.send(b"##")

    def login(self, data):
        name = data.split(" ")[1]
        password = data.split(" ")[-1]
        if self.db.login(name, password):
            self.connfd.send(b"OK")
        else:
            self.connfd.send(b"FAIL")


def main():
    sockfd = socket()
    # 设置端口立即释放
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(ADDR)
    sockfd.listen(5)
    print("listen port", ADDR)
    # 处理僵尸进程
    signal(SIGCHLD, SIG_IGN)
    while True:
        try:
            connfd, addr = sockfd.accept()
            print("connect from", addr)
        except:
            sockfd.close()
            break
        p = OnlineDict(connfd)
        p.daemon = True
        p.start()


if __name__ == '__main__':
    main()
