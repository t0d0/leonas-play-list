import tornado


class LPLLogoutHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.clear_cookie("user")
        self.redirect("/")
