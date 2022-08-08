# coding:utf-8

import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.web
import sys

import lpl_handler
from lpl_db import user_db, content_db, favorite_db
from lpl_const import config, secret

sys.path.append('/')


class LPLApplication(tornado.web.Application):
    def __init__(self, handlers, **settings):
        self.content_db = content_db.ContentDb()
        self.user_db = user_db.UserDb()
        self.favorite_db = favorite_db.FavoriteDb()
        self.salt = secret.salt
        tornado.web.Application.__init__(self, handlers, **settings)


# TODO:ハンドラーへのルーティングを整理したい。
application = LPLApplication([
    (r'/', lpl_handler.lpl_index_handler.LPLIndexHandler),
    (r'/?search', lpl_handler.lpl_index_handler.LPLIndexHandler),
    (r'/list.*', lpl_handler.lpl_list_handler.LPLListHandler),
    (r'/login.*', lpl_handler.lpl_login_handler.LPLLoginHandler),
    (r'/logout.*', lpl_handler.lpl_logout_handler.LPLLogoutHandler),
    (r'/create-account.*', lpl_handler.lpl_create_account_handler.LPLCreateAccountHandler),
    (r'/password-forgot.*', lpl_handler.lpl_password_forgot_handler.LPLPasswordForgotHandler),
    (r'/password-update.*', lpl_handler.lpl_password_update_handler.LPLPasswordUpdateHandler),
    (r'/api/favorite.*', lpl_handler.lpl_api_favorite_handler.LPLAPIFavoriteHandler),
    (r'/good.*', lpl_handler.lpl_good_handler.LPLGoodHandler),
    (r'/api/content.*', lpl_handler.lpl_api_content_handler.LPLAPIContentHandler),
    (r'/null', lpl_handler.lpl_index_handler.LPLIndexHandler),
],
    template_path=os.path.join(os.getcwd(), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug=True,
    cookie_secret=secret.cookie_secret,
    xsrf_cookies=True
)

if __name__ == "__main__":
    server_port = config.port
    print("server start:" + str(server_port))
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(server_port)
    tornado.ioloop.IOLoop.current().start()
