#!/usr/bin/python  
#coding:utf-8  

import logging
import os.path
import uuid
import socket
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import time
import json

import pdb



def send_message_ws(message):
    for handler in CodeSocketHandler.socket_handlers:
        try:
            handler.write_message(message)
                
        except:
            logging.error('Error sending message', exc_info=True)


def send_message_lp(message):
    for handler in CodeSocketHandler.socket_handlers:
        try:
            handler.write_message(message)
        except:
            logging.error('Error sending message', exc_info=True)

    for callback in CodePollHandler.callbacks:
        try:
            callback(message)
        except:
            logging.error('Error in callback', exc_info=True)
    CodePollHandler.callbacks = set()


class CodePollHandler(tornado.web.RequestHandler):
    #clear callbacks
    callbacks = set()

    #@tornado.web.asynchronous
    def get(self):
        CodePollHandler.callbacks.add(self.on_new_message)

    def on_new_message(self, message):
        if self.request.connection.stream.closed():
            return
        self.write(message)
        self.finish()

    def on_connection_close(self):
        CodePollHandler.callbacks.remove(self.on_new_message)
        #CodePollHandler.users.discard(self.user)
        #send_message_lp('A user has left the long poll chat room.')


    def post(self):

        CodePollHandler.callbacks.add(self.on_new_message)

        body = self.request.body

        req = json.loads(body)

        #data = self.get_body_argument('data')

        #return as a json message
        message = { 'source': req['source'],
                    'data': req['data']
                }

        print(message)
        send_message_lp(message)



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        logging.info("get index")
        self.render('index.html')


class CodeSocketHandler(tornado.websocket.WebSocketHandler):
    socket_handlers = set()

    def open(self):
        logging.debug("open socket")  
        CodeSocketHandler.socket_handlers.add(self)

    def on_close(self):
        CodeSocketHandler.socket_handlers.remove(self)
        send_message_ws('A user has left the socket chat room.')

    def on_message(self, message):
        logging.debug(message)

        request = json.loads(message)

        try:
            source = request['source']
            action = request['action']
            data = request['data']
        except:
            send_message_ws(json.dumps({'source':'console', 'data': message}))
            return

        req = { 'source': source,
                'action': action,
                'data': data
        }

        ret = self.remote_run(json.dumps(req))

        output = self.parse(ret)

        send_message_ws(json.dumps({'source':source, 'data': output}))

    def parse(self, data):
        lines = data.splitlines()
        msg = ''

        for line in lines:
            msg = msg + '<div>' + line + '</div>'

        return msg 

    def check_origin(self, origin): 
        logging.debug("check orgin true")       
        return True

    def remote_run(self, req):

        gdb_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        gdb_sock.connect(("localhost", 9999))

        #gdb_cmd = 'gdb,' + req.POST['gdb_cmd']
        output = self.gdb_command(gdb_sock, req)

        gdb_sock.close()

        return output

    def gdb_command(self, sock, cmd):
        sock.sendall(bytearray(cmd + "\n", "utf-8"))
        received = str(sock.recv(4096))
        return received

def send_test():
    i = 0
    while True:
        send_message_ws(str(i))
        i = i + 1
        time.sleep(1)


def main():
    #thread.start_new_thread(send_test, ())

    logging.basicConfig(level=logging.DEBUG)
    logging.debug('This message should go to the log file')
    logging.info('So should this')

    settings = {
        'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
        'static_path': os.path.join(os.path.dirname(__file__), 'static')
    }
    application = tornado.web.Application(
        [('/', MainHandler), ('/post', CodePollHandler), ('/socket', CodeSocketHandler)], **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
