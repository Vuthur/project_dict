from socket import *


class ClientHandle:
    def __init__(self):
        self.__client = socket()
        self.__ser_addr = ("127.0.0.1", 8888)
        self.connect()

    def connect(self):
        self.__client.connect(self.__ser_addr)

    def enroll(self):
        while True:
            name = input("请输入注册用户名:")
            self.__client.send(f"ENROLL U {name}".encode())
            data = self.__client.recv(1024)
            if data == b"ok":
                password = input("请设置密码:")
                password1 = input("请确认密码:")
                if password == password1:
                    self.__client.send(f"ENROLL P {name} {password}".encode())
                    data = self.__client.recv(1024)
                    print(data.decode())
                    break
            elif data == b"fail":
                print("用户名已存在, 请重新输入")

    def login(self):
        while True:
            name = input("请输入用户名:")
            password = input("请输入你的密码")
            self.__client.send(f"LOGIN {name} {password}".encode())
            data = self.__client.recv(1024)
            if data == b"n_wrong":
                print("用户名错误")
            elif data == b"p_wrong":
                print("用户名或密码错误")
            elif data == b"ok":
                print("登录成功")
                return True, name

    def exit(self):
        self.__client.close()

    def sesrch(self, name):
        while True:
            word = input("请输入要查询的单词:")
            if not word:
                break
            msg = f"FIND {word} {name}"
            self.__client.send(msg.encode())
            data = self.__client.recv(1024)
            if data == b"fail":
                print("未查询到该单词")
            else:
                print(data.decode())

    def history(self, name):
        msg = f"HIS {name}"
        self.__client.send(msg.encode())
        while True:
            his = self.__client.recv(1024).decode()
            if his == "done":
                break
            print(his)

    def logout(self):
        msg = f"LOGOUT "
        self.__client.send(msg.encode())


class ClientView:
    def __init__(self):
        self.__handle = ClientHandle()

    def __view1(self):
        print("======")
        print("注册: 1")
        print("登录: 2")
        print("退出: 3")
        print()

    def __view2(self):
        print("======")
        print("查询: 1")
        print("历史: 2")
        print("注销: 3")
        print()

    def __choice(self, choice):
        if choice == "1":
            self.__handle.enroll()
        elif choice == "2":
            jugement, name = self.__handle.login()
            if jugement:
                self.__sub_main(name)
        elif choice == "3":
            self.__handle.exit()

    def __choice2(self, choice, name):
        if choice == "1":
            self.__handle.sesrch(name)
        elif choice == "2":
            self.__handle.history(name)
        elif choice == "3":
            self.__handle.logout()

    def __sub_main(self, name):
        while True:
            self.__view2()
            choice = input("请输入你的选项")
            self.__choice2(choice, name)
            if choice == "3":
                break

    def main(self):
        while True:
            self.__view1()
            selection = input("请输入你要选择的功能:")
            self.__choice(selection)
            if selection == "3":
                break


if __name__ == '__main__':
    client = ClientView()
    client.main()