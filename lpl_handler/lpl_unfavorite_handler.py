import tornado


class LPLUnFavoriteHandler(tornado.web.RequestHandler):
    def post(self):
        print('un favorite')
        user = self.get_secure_cookie("user").decode('utf-8')
        target_id = self.get_argument('target')
        self.application.favorite_dba.remove_data(user, target_id)
        #        data = list(content_dba.get_data())
        #        self.redirect("/leonas_play_list")
        self.write("favorite")
