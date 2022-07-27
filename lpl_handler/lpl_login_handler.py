import tornado

from lpl_util import util


class LPLLoginHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        #        print('index_get')
        #        search_word = ''
        #        search_word = self.get_argument('search', '')
        self.render("login.html")

    def post(self):
        e_mail = self.get_argument('e-mail')
        password = util.get_hashed_password(self.get_argument('password'), self.application.salt)
        user = self.application.user_dba.get_data(e_mail, password)
        if user is not None:
            self.set_secure_cookie("user", e_mail)
            self.redirect("/")
        else:
            self.render("login.html")
