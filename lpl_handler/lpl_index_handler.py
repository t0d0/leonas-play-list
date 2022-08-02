import json
import tornado

from lpl_util import util


class LPLIndexHandler(tornado.web.RequestHandler):
    def get(self):
        print('index_get')
        favorite_flg = self.get_argument('favorite', '') == 'true'
        login_flg = False
        user = self.get_secure_cookie("user")
        if user:
            login_flg = True
        self.render("index.html", login_flg=login_flg, favorite_flg=favorite_flg)

