import pymongo
import tornado

from lpl_util import util


class LPLCreateAccountHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("create_account.html")

    def post(self):
        e_mail = self.get_argument('e-mail')
        password = util.get_hashed_password(self.get_argument('password'), self.application.salt)
        try:
            self.application.user_dba.set_data({
                "e-mail": e_mail,
                "password": password
            })
        except pymongo.errors.DuplicateKeyError:
            print('登録済みユーザ')
            self.render("create_account.html", message='このメールアドレスは登録済みです')
        self.redirect("/login")
