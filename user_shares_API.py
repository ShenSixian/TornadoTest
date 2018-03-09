import tornado.web
import pymysql
class UserShareHandler(tornado.web.RequestHandler):
	"""operate user data: load_data, add, delete"""
	def set_default_headers(self):
		print("setting headers!!!")
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

	def post(self):
		order = self.get_argument("order")
		self.username = self.get_argument("username")
		# prepare database
		self.db = pymysql.connect("localhost","root","root1234","mytest", charset="utf8")
		self.cursor = self.db.cursor()
		# switch order
		if (order == "load_data"):
			self.write(self.load_data())
		elif (order == "add"):
			self.write(self.add(self.get_argument("code")))
		elif (order == "delete"):
			self.write(self.delete(self.get_argument("code")))

		self.db.close()


	def load_data(self):
		# load user's all share data
		sql = "SELECT * FROM %s" %(self.username)
		results = {'values': [], 'status': ''}
		try:
			self.cursor.execute(sql)
			lines = self.cursor.fetchall()
			for line in lines:
				# get detail data of share from table SHARES
				sql = "SELECT * FROM shares WHERE code = %s" %(line[0])
				self.cursor.execute(sql)
				data = self.cursor.fetchone()
				result  = {}
				result['name'] = data[0]
				result['code'] = data[1]
				result['latestprice'] = data[2]
				results['values'].append(result)
			results['status'] = "OK"
		except:
			results['status'] = "ERROR"
			print("error!")
		return results

	def add(self,code):
		# if exist in total shares
		# return status 'OK' or 'ERROR' and the values of the share
		sql = "SELECT * FROM shares WHERE code = %s" %str(code)
		try:
			self.cursor.execute(sql)
			data = self.cursor.fetchone()
			result = {'values': {},'status': ''}
			if (data): # exist in shares table (all)
				# add code into the share table of user
				sql = "INSERT INTO %s (code) VALUES ('%s')" %(self.username, code)
				self.cursor.execute(sql)
				self.db.commit()
				# get detail information
				result['values']['name'] = data[0]
				result['values']['code'] = data[1]
				result['values']['latestprice'] = data[2]
				result['status'] = "OK"
			else:
				result['status'] = "ERROR"
		except:
			self.db.rollback()
			print("error!")
			result['status'] = "ERROR"
		return result

	def delete(self, code):
		# delete the code in the share table
		# return 'OK' or 'ERROR'
		sql = "DELETE FROM %s WHERE code = %s" % (self.username, code)
		try:
			self.cursor.execute(sql)
			self.db.commit()
			return {'status': 'OK'}
		except:
			self.db.rollback()
			print("error!")
			return {'status': 'ERROR'}