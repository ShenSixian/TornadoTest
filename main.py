import tornado.ioloop
from tornado.options import define, options
import tornado.web
from loginAPI import LoginHandler
from klineAPI import KLineDataHandler
from share_data_API import DataHandler
from user_shares_API import UserShareHandler
from registerAPI import RegisterHandler
define("port", default=8888, help="run on the given port", type=int)

HANDLERS = [
    (r"/ajax/login", LoginHandler),
    (r"/ajax/kline", KLineDataHandler),
    (r"/ajax/share_data", DataHandler), # 获取所有股票信息
    (r"/ajax/user_shares", UserShareHandler),  # user share data operation
    (r"/ajax/register", RegisterHandler) 
]
application = tornado.web.Application(handlers=HANDLERS)
if __name__ == "__main__":
    application.listen(options.port)
    print("Starting development server at http://127.0.0.1:"+str(options.port))
    print("Quit the server with CONTROL-C.")
    tornado.ioloop.IOLoop.instance().start()