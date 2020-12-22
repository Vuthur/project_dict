from pymysql import *


# 注意 connect 传参一定需要关键字传参
class SerDatabase:
    def __init__(self):
        self.host = "localhost"
        self.port = 3306
        self.user = "root"
        self.password = "123456"
        self.database = "dict"
        self.charset = "utf8"
        self.db = self.connect()
        self.cur = self.cursor()

    def connect(self):
        db = connect(host=self.host, port=self.port, user=self.user, password=self.password,
                     database=self.database, charset=self.charset)
        return db

    def cursor(self):
        cur = self.db.cursor()
        return cur

    def juge_user(self, name):
        sql = "select name from users where name = '%s'" % name
        self.cur.execute(sql)
        if self.cur.fetchone():
            return False
        return True

    def storage_user(self, name, passwd):
        sql = "insert into users (name, passwd) values (%s, %s);"
        self.cur.execute(sql, (name, passwd))
        self.db.commit()

    def juge_passwd(self, name, passwd):
        sql = "select passwd from users where name = '%s';" % name
        self.cur.execute(sql)
        if self.cur.fetchone()[0] == passwd:
            return True
        return False

    def word_mean(self, word):
        sql = "select mean from words where word = '%s'" % word
        self.cur.execute(sql)
        mean_list = self.cur.fetchone()
        if mean_list: return mean_list[0]
        return None

    def sto_history(self, name, word):
        sql = "insert into history (name, word) values (%s, %s);"
        self.cur.execute(sql, (name, word))
        self.db.commit()

    def select_his(self, name):
        sql = "select name, word, time from history where name = '%s';" % name
        self.cur.execute(sql)
        his = self.cur.fetchmany(10)
        if his: return his
        return None


if __name__ == '__main__':
    user = SerDatabase()
    a = user.select_his("wu")
    if a:
        for b in a:
            print(b)