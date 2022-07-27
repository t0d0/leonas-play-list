import json

import tornado

from lpl_util import util


class LPLEditHandler(tornado.web.RequestHandler):
    def post(self):
        print('edit')
        update_data = {
            "_id": self.get_argument('target'),
            "title": self.get_argument('title'),
            "artist": self.get_argument('artist'),
            "video_id": util.get_video_id(self.get_argument('url')),
            "time": util.convert_time(self.get_argument('time'))
        }

        self.application.content_dba.update_data(update_data)

        #        data = list(content_dba.get_data())
        #        self.redirect("/leonas_play_list")
        self.write(json.dumps(update_data))
