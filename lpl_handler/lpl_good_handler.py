import tornado


# TODO:未使用のため、削除予定
class LPLGoodHandler(tornado.web.RequestHandler):
    def post(self):
        print('good')
        target_id = self.get_argument('target')
        self.application.content_dba.increment_good(target_id)
        #        data = list(content_dba.get_data())
        self.redirect("/leonas_play_list")
