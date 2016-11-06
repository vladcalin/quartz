import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.log

from eventer.settings import SERVER_HOST, SERVER_PORT
from eventer.handlers.user_handlers import UserCreationApiHandler, CreateNewTokenHandler, RevokeTokenHandler, \
    AuthenticateUserHandler, LogoutUserHandler, GetUserInfoHandler
from eventer.handlers.base import ErrorHandler


def make_app(app_settings):
    return tornado.web.Application([
        # user-related api
        (r"/api/users/create", UserCreationApiHandler),  # POST, public
        (r"/api/users/api_tokens/create", CreateNewTokenHandler),  # POST, private
        (r"/api/users/api_tokens/revoke", RevokeTokenHandler),  # POST, private
        (r"/api/users/authenticate", AuthenticateUserHandler),  # POST, public
        (r"/api/users/logout", LogoutUserHandler),  # POST, private
        (r"/api/users/info", GetUserInfoHandler),  # POST, private

    ], **app_settings)


if __name__ == '__main__':
    settings = {
        "static_path": os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"),
        "template_path": os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"),
        "cookie_secret": "!$FF#@T&%NRfWG%$h6J45t2#!deDSBn7j5^g43dQWadFDBn7^7%$r",
        "xsrf_cookies": False,
        "default_handler_class": ErrorHandler,
        "default_handler_args": dict(status_code=404),

        # debug
        "debug": True,
        # "autoreload": True
    }
    tornado.log.enable_pretty_logging()

    server = tornado.httpserver.HTTPServer(make_app(settings))
    server.bind(SERVER_PORT)
    server.start()
    tornado.ioloop.IOLoop.current().start()
