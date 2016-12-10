import tornado.httpserver
import tornado.web
from   tornado.options import options,define
import tornado.ioloop
import os.path
from handler import *

define("port", default=8899, help="run on give port", type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r'/login', login),
			(r'/list', tlist),
			(r'/toEval', toEval),
			(r'/EvalResult', ResultShow)
		]
		
		settings = dict(
			template_path = os.path.join(os.path.dirname(__file__), "templates"),
			static_path = os.path.join(os.path.dirname(__file__), "static"),
			debug = True,
			autoreload = True,
			cookie_secret="feljjfesrh48thfe2qrf3np2zl90bmwj",
			xsrf_cookie=True,
		)

		tornado.web.Application.__init__(self, handlers = handlers, **settings)

if __name__ == "__main__":
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
