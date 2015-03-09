#!/usr/bin/python  
#coding:utf-8  

import logging
import os.path
import uuid
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import time


def send_message_ws(message):
    for handler in ChatSocketHandler.socket_handlers:
        try:
            handler.write_message(message)
        except:
            logging.error('Error sending message', exc_info=True)


def send_message_lp(message):
    for handler in ChatSocketHandler.socket_handlers:
        try:
            handler.write_message(message)
        except:
            logging.error('Error sending message', exc_info=True)

    for callback in ChatPollHandler.callbacks:
        try:
            callback(message)
        except:
            logging.error('Error in callback', exc_info=True)
    ChatPollHandler.callbacks = set()


class ChatPollHandler(tornado.web.RequestHandler):
    callbacks = set()
    users = set()

    @tornado.web.asynchronous
    def get(self):
        ChatPollHandler.callbacks.add(self.on_new_message)
        self.user = user = self.get_cookie('user')
        if not user:
            self.user = user = str(uuid.uuid4())
            self.set_cookie('user', user)
        if user not in ChatPollHandler.users:
            ChatPollHandler.users.add(user)
            send_message_lp('A new user has entered the long pollchat room.')

    def on_new_message(self, message):
        if self.request.connection.stream.closed():
            return
        self.write(message)
        self.finish()

    def on_connection_close(self):
        ChatPollHandler.callbacks.remove(self.on_new_message)
        ChatPollHandler.users.discard(self.user)
        send_message_lp('A user has left the long poll chat room.')

    def post(self):
        send_message_lp(self.get_argument('text'))


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        logging.warning("get index")
        self.render('index.html')


class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    socket_handlers = set()

    def open(self):
        logging.debug("open socket")  
        ChatSocketHandler.socket_handlers.add(self)

    def on_close(self):
        ChatSocketHandler.socket_handlers.remove(self)
        send_message_ws('A user has left the socket chat room.')

    def on_message(self, message):
        send_message_ws(message)

    def check_origin(self, origin): 
        logging.debug("check orgin true")       
        return True


def send_test():
    i = 0
    while True:
        send_message_ws(str(i))
        i = i + 1
        time.sleep(1)


def main():
    #thread.start_new_thread(send_test, ())
    settings = {
        'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
        'static_path': os.path.join(os.path.dirname(__file__), 'static')
    }
    application = tornado.web.Application(
        [('/', MainHandler), ('/poll', ChatPollHandler), ('/socket', ChatSocketHandler)], **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()