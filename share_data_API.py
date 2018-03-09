import tornado.web
import pymysql
class DataHandler(tornado.web.RequestHandler):
	def set_default_headers(self):
		print("setting headers!!!")
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

	def post(self):
		results = {}
		results['data'] = self.load_data()
		self.write(results)

	def load_data(self):
		db = pymysql.connect("localhost","root","root1234","mytest", charset="utf8")
		cursor = db.cursor()
		sql = "SELECT * FROM shares"
		results = []
		try:
			cursor.execute(sql)
			rows = cursor.fetchall()
			for row in rows:
				result  = {}
				result['name'] = row[0]
				result['code'] = row[1]
				result['latestprice'] = row[2]
				results.append(result)
		except:
			print("error!")
		db.close()
		return results