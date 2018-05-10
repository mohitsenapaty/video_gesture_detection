#s a Tornado web server with a django project
# Make sure to edit the DJANGO_SETTINGS_MODULE to point to your settings.py
#
# http://localhost:8080/hello-tornado
# http://localhost:8080

import sys
import os

from tornado.options import options, define, parse_command_line
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
import tornado.websocket
import tornado.gen
import json
from django.core.wsgi import get_wsgi_application
from decimal import Decimal

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")


define('port', type=int, default=8000)
#text_data = ""

class text_class(object):
  text_str = ""
  @classmethod
  def update_str(self,txt):
    self.text_str+="</br>"+txt
  @classmethod
  def get_str(self):
    return self.text_str

class WSHandler(tornado.websocket.WebSocketHandler):

  clients = []
  text_data = ""

  def open(self):
    print 'New connection was opened'
    #self.write_message("Conn! " + text_class.get_str())
    self.write_message(text_class.get_str())
    self.clients.append(self)

  @tornado.web.asynchronous
  @tornado.gen.coroutine
  def on_message(self, message):
    #import pdb; pdb.set_trace();
    print 'Got :', message
    quote = ast.literal_eval(message)
    quote['timestamp'] = datetime.datetime.now()
    quote['price'] = Decimal(quote['price'])
    quote['quantity'] = Decimal(quote['quantity'])
    global queue
    queue.put(quote)
    if quote['instrument'] == "BTC_INR":
        global OrderBook_Bitcoin
        trades = OrderBook_Bitcoin.process_order(quote,False)
    elif quote['instrument'] == "ETH_INR":
        global OrderBook_Eth
        trades = OrderBook_Eth.process_order(quote,False)
    elif quote['instrument'] == "XRP_INR":
        global OrderBook_Ripple
        trades = OrderBook_Ripple.process_order(quote,False)
    elif quote['instrument'] == "BCH_INR":
        global OrderBook_BitCash
        trades = OrderBook_BitCash.process_order(quote,False)
    else:
        sys.exit("Incorrect Instrument Type")
    if trades:
        print trades
    #glob text_data
    #self.text_data += message
    #self.write_message("Received: " + message)
    text_class.update_str(message)
    for i in range(0,len(self.clients)):
      if i%10 == 0:
        yield tornado.gen.moment
      self.clients[i].write_message( text_class.get_str())
    print text_class.get_str()

  def on_close(self):
    #print 'Conn closed...'
    self.clients.remove(self)


class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello from tornado')



def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'exchange.settings' # TODO: edit this
    sys.path.append('./../exchange') # path to your project if needed
    
    P = multiprocessing.Process(target=push_to_db)
    P.start()

    parse_command_line()

    wsgi_app = get_wsgi_application()
    container = tornado.wsgi.WSGIContainer(wsgi_app)
    handlers = [
            (r'/ws/', WSHandler),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path':static_path}),
            ('/hello', HelloHandler),
            ('.*', tornado.web.FallbackHandler, dict(fallback=container)),
    ]
    tornado_app = tornado.web.Application(handlers)

    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port)

    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
