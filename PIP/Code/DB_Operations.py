import pymysql
import sys

class Database:
    def __init__(self, db):
        host = "cibc-poc-db.chyyhhx84xlq.us-east-2.rds.amazonaws.com"
        user = "admin"
        pwd = "cibcproject"
        self.db = db
        self.con = pymysql.connect(host=host, user=user, password=pwd, db=db, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()

    def insert(self, query, values):
        try:
            self.cur.execute(query, values)
            self.con.commit()
            return 200
        except pymysql.Error as e:
            raise e.with_traceback(sys.exc_info()[2])

    def query(self, query, values=None):
        try:
            if values is not None:
                self.cur.execute(query, values)
            else:
                self.cur.execute(query)
            result = self.cur.fetchall()  # gets all tuples from the result of the execute above
        except pymysql.Error as e:
            raise e.with_traceback(sys.exc_info()[2])
        return result




