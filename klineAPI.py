import tornado.web
import tushare as ts

class KLineDataHandler(tornado.web.RequestHandler):
	def set_default_headers(self):
		print("setting headers!!!")
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

	def post(self):
		code = self.get_argument('code')
		data = {}
		data['date'],data['values'] = self.get_data(code)
		self.write(data)

	def get_data(self,code):
		data_lines = ts.get_k_data(code).get_values()
		date = []
		values = []
		for line in data_lines:
			date.append(line[0])
			value = [line[1],line[2],line[3],line[4]]
			values.append(value)
		return date,values
