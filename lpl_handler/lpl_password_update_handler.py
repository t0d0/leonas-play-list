import tornado


# TODO:未実装
class LPLPasswordUpdateHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("password_update.html")

    def post(self):
        #        print('index_post')
        self.render("password_update.html")
