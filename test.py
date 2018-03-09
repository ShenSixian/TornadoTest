import pymysql
user = 'adin'
psw = '123'
sql = "SELECT * FROM users WHERE username = '%s' AND password = '%s'" %(user, psw)
db = pymysql.connect("localhost","root","root1234","mytest", charset="utf8")
cursor = db.cursor()
print(sql)
cursor.execute(sql)
result = cursor.fetchone()
print(result)
db.close()