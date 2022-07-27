import tornado


class LPLFavoriteHandler(tornado.web.RequestHandler):
    def post(self):
        print('favorite')
        user = self.get_secure_cookie("user").decode('utf-8')
        #        print(user)
        target_id = self.get_argument('target')
        #        print(target_id)
        self.application.favorite_dba.set_data(user, target_id)
        self.write("favorite")

