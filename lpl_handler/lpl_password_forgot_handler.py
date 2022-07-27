import tornado


# TODO:未実装
class LPLPasswordForgotHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        #        print('index_get')
        #        search_word = ''
        #        search_word = self.get_argument('search', '')
        self.render("password_forgot.html")

    def post(self):
        #        print('index_post')
        self.render("password_forgot.html")
