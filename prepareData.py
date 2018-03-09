from sqlalchemy import create_engine
import tushare as ts
import pymysql

def creatDB(cursor):
	"""创建数据库"""
	cursor.execute("DROP TABLE IF EXISTS shares")
	sql = """CREATE TABLE shares (
	         name  CHAR(20),
	         code  CHAR(20), 
	         price FLOAT(20))"""
	cursor.execute(sql)

def insertData(cursor,number):
	"""向数据库插入NUMBER条数据"""
	i = 0
	stock_list = ts.get_stock_basics()	
	for code,info in stock_list.iterrows():
		df = ts.get_realtime_quotes(code).get_values()
		sql = "INSERT INTO shares(code,name,price) VALUES ('%s', '%s', '%.2f')" % (code, info[1], float(df[0][3]))
		try:
			cursor.execute(sql)
			db.commit()
		except:
			print("error")
		i += 1
		if (i > number):
			break

if __name__ == '__main__':
	db = pymysql.connect("localhost","root","root1234","mytest", charset="utf8")
	cursor = db.cursor()
	creatDB(cursor)
	insertData(cursor,100)
	db.close()