import pymysql
from encrypted import MD5


class DictTable:
    def __init__(self):
        self.db = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="123456",
            database="dict",
            charset="utf8"
        )

    def close(self):
        # 关闭游标和数据库连接
        self.cur.close()
        self.db.close()

    def cursor(self):
        # 创建游标 (执行sql语句获取执行结果的对象)
        self.cur = self.db.cursor()

    def register(self, name, password):
        sql = "select name from user where name=%s;"
        self.cur.execute(sql, [name])
        result = self.cur.fetchone()
        if result:
            # 如果result不为假说明用户已存在
            return False
        else:
            try:
                sql = "insert into user (name,password) values (%s, %s);"
                self.cur.execute(sql, [name, MD5(password)])
                self.db.commit()
                return True
            except Exception as e:
                print(e)
                self.db.rollback()
                return False

    def find_word(self, name, word):
        sql = "select translation from words where word = %s;"
        self.cur.execute(sql, [word])
        mean = self.cur.fetchone()
        sql = "select id from user where name=%s;"
        self.cur.execute(sql, [name])
        user_id = self.cur.fetchone()[0]
        sql = "insert into history (word,user_id) values (%s, %s)"
        self.cur.execute(sql, [word, user_id])
        self.db.commit()
        return mean

    def history(self, name):
        sql = "select name, word, time " \
              "from user left join history " \
              "on user.id=history.user_id " \
              "where name=%s " \
              "order by time desc " \
              "limit 10;"
        self.cur.execute(sql, [name])
        result = self.cur.fetchall()
        return result

    def login(self, name, passowrd):
        sql = "select * from user where name=%s and password=%s;"
        self.cur.execute(sql, [name, MD5(passowrd)])
        result = self.cur.fetchone()
        if result:
            return True
        else:
            return False
