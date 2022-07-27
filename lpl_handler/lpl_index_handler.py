import json
import tornado

from lpl_util import util


class LPLIndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        print('index_get')
        favorite_flg = self.get_argument('favorite', '') == 'true'
        login_flg = False
        user = self.get_secure_cookie("user")
        if user:
            login_flg = True
        self.render("index.html", login_flg=login_flg, favorite_flg=favorite_flg)

    def post(self):
        titles = util.split_vertical_bar(self.get_argument('title'))
        times = util.split_vertical_bar(self.get_argument('time'))

        inserted_ids = []
        for (title, time) in zip(titles, times):
            data = {
                'title': title,
                'time': util.convert_time(time),
                'video_id': util.get_video_id(self.get_argument('url'))
            }
            inserted_ids.append(str(self.application.content_db.set_data(data).inserted_id))

        content_data_list = []
        for inserted_id in inserted_ids:
            content_data_list.extend(list(self.application.content_db.get_data_by_id(inserted_id)))
        print(content_data_list)
        for data in content_data_list:
            data['_id'] = str(data['_id'])

        self.write(json.dumps(content_data_list))
