import json

import tornado

from lpl_util import util


class LPLEditHandler(tornado.web.RequestHandler):
    async def post(self):
        print('edit')
        content_db = self.application.content_db
        update_data = content_db.DataFormat(_id=self.get_argument('target'),
                                            title=self.get_argument('title'),
                                            artist=self.get_argument('artist'),
                                            video_id=util.get_video_id(self.get_argument('url')),
                                            time=util.convert_time(self.get_argument('time')))

        update_result = await content_db.update_data(update_data)
        for i, data in enumerate(update_result):
            print(update_result[i])
            update_result[i]['_id'] = str(data['_id'])

        print(update_result)
        print(type(update_result))
        self.write(json.dumps(update_result[0]))
