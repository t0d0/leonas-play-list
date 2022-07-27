import json

import tornado


class LPLDeleteHandler(tornado.web.RequestHandler):
    def post(self):
        print('delete')
        target_id = self.get_argument('target')
        self.application.content_dba.erase_data(target_id)
        #        data = list(content_dba.get_data())
        #        self.redirect("/leonas_play_list")
        self.write(json.dumps({"result": "complete"}))

