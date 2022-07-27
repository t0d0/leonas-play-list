import tornado

from lpl_util import util


class LPLListHandler(tornado.web.RequestHandler):
    def get(self):
        print('list_get')
        title_list = list(self.application.content_dba.get_title_list())
        artist_list = list(self.application.content_dba.get_artist_list())

        title_list = util.sort_dict_list(title_list, 'title')
        artist_list = util.sort_dict_list(artist_list, 'artist')
        #        self.write(json.dumps(list(content_dba.get_title_list()),ensure_ascii=False))
        login_flg = False
        user = self.get_secure_cookie("user")
        if user:
            login_flg = True
        self.render("title_list.html", title_list=title_list, login_flg=login_flg, artist_list=artist_list)
