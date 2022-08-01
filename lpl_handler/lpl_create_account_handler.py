import pymongo
import tornado

from lpl_util import util


class LPLCreateAccountHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("create_account.html")

    async def post(self):
        user_db = self.application.user_db
        password = util.get_hashed_password(self.get_argument('password'), self.application.salt)
        e_mail = self.get_argument('e-mail')
        user_data = user_db.DataFormat(
            e_mail=e_mail,
            password=password,
            _id=e_mail
        )

        user_regist_result = await user_db.set_data(user_data)
        if user_regist_result is None:
            self.render("create_account.html", message='このメールアドレスは登録済みです')
        else:
            self.redirect("/login")
