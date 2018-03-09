import tornado.web
import pymysql
class RegisterHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        print ("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        
    def get(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        self.write(self.register(username,password))

    def register(self, user, psw):
        db = pymysql.connect("localhost","root","root1234","mytest", charset="utf8")
        cursor = db.cursor()
        if (self.isExistence(user,psw,cursor)):
            print(3)
            return {'status': 'REREGISTER'}
        sql1 = "INSERT INTO users (username, password) VALUES ('%s', '%s')" %(user, psw)
        sql2 = "CREATE TABLE %s (code  CHAR(6))" %(user)
        try:
            cursor.execute(sql1)
            cursor.execute(sql2)
            db.commit()
        except:
            db.rollback()
            print("error!")
            return {'status': 'ERROR'}
        db.close()
        return {'status': 'OK'}

    def isExistence(self,user,psw, cursor):
        sql = "SELECT * FROM users WHERE username = '%s'" %(user)
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            if (result):
                return True
            else:
                return False
        except:
            print("ERROR!")
            return True
        
