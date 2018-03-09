import tornado.web
import pymysql
import hashlib
import time
class LoginHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        print ("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        
    def get(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        print(username,password)
        if (self.validate(username,password)):
            obj = hashlib.md5()                                     #创建md5加密对象
            obj.update(bytes(str(time.time()),encoding = "utf-8"))  
            # container = {} 
            session = obj.hexdigest()
            # container[session] = {}
            # container[session]['username'] = username        
            # container[session]['password'] = password           
            # container[session]['is_login'] = True                
            self.set_cookie('cookie',session,expires_days=1)    #将密串作为cookie值写入浏览器
            self.write("OK")
        else:
            self.write("ERROR")


    def validate(self,name,psw):
        db = pymysql.connect("localhost","root","root1234","mytest", charset="utf8")
        cursor = db.cursor()
        sql = "SELECT * FROM users WHERE username = '%s' AND password = '%s'" %(name, psw)
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            db.close()
            if (result == 'None'):
                return False
            return True
            # if results == None:
            #     return False
            # else:
            #     return True
        except:
            print("error!")
            return False