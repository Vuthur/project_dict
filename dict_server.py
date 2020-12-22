from dict_mysql import SerDatabase
from socket import *
from select import select
from time import sleep
from multiprocessing import Process

# class SerProcess(Process):
#     def __init__(self, sock):
#         super().__init__(daemon=True)
#         self.sock = sock
#         self.__handle = Handle()
#
#
#     def run(self):
#         while True:
#             data = self.sock.recv(1024)
#             if not data:
#                 self.sock.close()
#                 break
#             self.__handle.request(self.sock, data)



class Server:
    def __init__(self, addr=("0.0.0.0", 18888)):
        self.addr = addr
        self.__tcpsock = socket()
        self.__bind()
        self.__litsen()

    def __bind(self):
        self.__tcpsock.bind(self.addr)

    def __litsen(self):
        self.__tcpsock.listen(5)

    def main(self):
        self.__tcpsock.setblocking(False)
        while True:
            try:
                client, addr = self.__tcpsock.accept()
                print(addr, "has connected.")
            except KeyboardInterrupt:
                self.__tcpsock.close()
                return
            p = SerProcess(client)
            p.start()


# class Server:
#     def __init__(self, addr=("0.0.0.0", 18888)):
#         self.addr = addr
#         self.__tcpsock = socket()
#         self.__bind()
#         self.__litsen()
#         self.__handle = Handle()
#         self.__rlist = [self.__tcpsock]
#         self.__wlist = []
#         self.__xlist = []
#
#     def __bind(self):
#         self.__tcpsock.bind(self.addr)
#
#     def __litsen(self):
#         self.__tcpsock.listen(5)
#
#     def main(self):
#         self.__tcpsock.setblocking(False)
#         while True:
#             rs, ws, xs = select(self.__rlist, self.__wlist, self.__xlist)
#             for sock in rs:
#                 if sock is self.__tcpsock:
#                     client, addr = sock.accept()
#                     print(addr, "has connected.")
#                     client.setblocking(False)
#                     self.__rlist.append(client)
#                 else:
#                     data = sock.recv(1024)
#                     if not data:
#                         sock.close()
#                         self.__rlist.remove(sock)
#                         continue
#                     self.__handle.request(sock, data)