import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.web

from eventer.handlers.ui import IndexHandler


def make_app(settings):
    return tornado.web.Application([
        # html routes
        (r'/', IndexHandler),

        # static routes
        (r'/static/(.*)', tornado.web.StaticFileHandler),

        # api routes
    ], **settings)


if __name__ == '__main__':
    settings = {
        "static_path": os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"),
        "template_path": os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"),
        "cookie_secret": "!$FF#@T&%NRfWG%$h6J45t2#!deDSBn7j5^g43dQWadFDBn7^7%$r",
    }

    server = tornado.httpserver.HTTPServer(make_app(settings))
    server.bind(8888)
    server.start()
    tornado.ioloop.IOLoop.current().start()
