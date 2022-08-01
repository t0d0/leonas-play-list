import tornado


class LPLFavoriteHandler(tornado.web.RequestHandler):
    async def post(self):
        print('favorite')
        user = self.get_secure_cookie("user").decode('utf-8')
        #        print(user)
        target_id = self.get_argument('target')
        # print(target_id)
        await self.application.favorite_db.set_data(user, target_id)
        self.write("favorite")

