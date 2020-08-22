from socket import *

# 全局变量
ADDR = ("0.0.0.0", 11111)


class OnlineDict:
    def __init__(self):
        self.sock = socket()
        self.sock.connect(ADDR)

    def first_menu(self):
        while True:
            print("""
        ====================
             1.注册
             2.登录
             3.退出
          tips：请输入序号
        ====================
        """)
            op = input("请输入选择：")
            if op == "1":
                result = self.register()
                if result:
                    print("注册成功")
                    self.second_menu(result)
                else:
                    print("注册失败.")

            elif op == "2":
                result = self.log_in()
                if result:
                    print("登录成功!!!")
                    self.second_menu(result)
                else:
                    print("用户名或密码有误")

            else:
                self.sock.send(b"Q")
                self.sock.close()
                return

    def second_menu(self, name):
        while True:
            print("""
        ====================
             1.查单词
             2.查看历史记录
             3.注销
          tips：请输入序号
        =====user:%s========
        """ % name)
            op = input("请输入选择：")
            if op == "1":
                self.find_words(name)
            elif op == "2":
                self.find_history(name)
            elif op == "3":
                return

    def register(self):
        while True:
            name = input("请输入名字：")
            password = input("请输入密码：")
            if " " in name or " " in password:
                print("名字或密码不能含有空格")
            else:
                break
        msg = "R " + name + " " + password
        self.sock.send(msg.encode())
        if self.sock.recv(2) == b"OK":
            return name
        else:
            return False

    def log_in(self):
        name = input("请输入名字：")
        password = input("请输入密码：")
        msg = "L " + name + " " + password
        self.sock.send(msg.encode())
        if self.sock.recv(2) == b"OK":
            return name
        else:
            return False

    def find_words(self, name):
        print("直接输入回车退出查单词.")
        while True:
            word = input("word:")
            if not word:
                return
            msg = "F " + name + " " + word
            self.sock.send(msg.encode())
            data = self.sock.recv(1024 * 10)
            if data != b"FAIL":
                print(data.decode())
            else:
                print("该单词不存在")


    def find_history(self, name):
        msg = "H " + name
        self.sock.send(msg.encode())
        msg = ""
        while True:
            data = self.sock.recv(1024)
            if data == b"##":
                print(msg, end="")
                return
            msg += data.decode()



def main():
    dictionary = OnlineDict()
    dictionary.first_menu()


if __name__ == '__main__':
    main()
