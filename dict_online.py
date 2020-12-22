from dict_mysql import SerDatabase
from socket import *
from select import select
from time import sleep


class Handle:
    def __init__(self):
        self.__userdata = SerDatabase()

    def enroll(self, sock, data_list):
        if data_list[1] == "U":
            if self.__userdata.juge_user(data_list[2]):
                sock.send(b"ok")
            else:
                sock.send(b"fail")
        elif data_list[1] == "P":
            self.__userdata.storage_user(data_list[2], data_list[3])
            sock.send("注册成功".encode())

    def login(self, sock, data_list):
        name = data_list[1]
        password = data_list[2]
        if self.__userdata.juge_user(name):
            sock.send(b"n_wrong")
        else:
            if self.__userdata.juge_passwd(name, password):
                sock.send(b"ok")
            else:
                sock.send(b"p_wrong")

    def find(self, sock, data_list):
        word = data_list[1]
        mean = self.__userdata.word_mean(word)
        if mean:
            sock.send(mean.encode())
        else:
            sock.send(b"fail")
        self.__userdata.sto_history(data_list[-1], word)

    def history(self, sock, data_list):
        tuple_his = self.__userdata.select_his(data_list[1])
        if tuple_his:
            for his in tuple_his:
                sleep(0.1)
                sock.send(str(his).encode())
        else:
            sock.send("目前无查询记录".encode())
        sleep(0.1)
        sock.send(b"done")

    def logout(self, sock):
        sock.close()

    def request(self, sock, data):
        data_list = data.decode().split(" ", 3)
        if data_list[0] == "ENROLL":
            self.enroll(sock, data_list)
        elif data_list[0] == "LOGIN":
            self.login(sock, data_list)
        elif data_list[0] == "FIND":
            self.find(sock, data_list)
        elif data_list[0] == "HIS":
            self.history(sock, data_list)
        elif data_list[0] == "LOGOUT":
            self.logout(sock)


class Server:
    def __init__(self, addr=("0.0.0.0", 8888)):
        self.addr = addr
        self.__tcpsock = socket()
        self.__bind()
        self.__litsen()
        self.__handle = Handle()
        self.__rlist = [self.__tcpsock]
        self.__wlist = []
        self.__xlist = []

    def __bind(self):
        self.__tcpsock.bind(self.addr)

    def __litsen(self):
        self.__tcpsock.listen(5)

    def main(self):
        self.__tcpsock.setblocking(False)
        while True:
            rs, ws, xs = select(self.__rlist, self.__wlist, self.__xlist)
            for sock in rs:
                if sock is self.__tcpsock:
                    client, addr = sock.accept()
                    print(addr, "has connected.")
                    client.setblocking(False)
                    self.__rlist.append(client)
                else:
                    data = sock.recv(1024)
                    if not data:
                        sock.close()
                        self.__rlist.remove(sock)
                        continue
                    self.__handle.request(sock, data)


if __name__ == '__main__':
    ser = Server()
    ser.main()
