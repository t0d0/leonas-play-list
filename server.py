# coding:utf-8
import asyncio
import os
import schedule
import time
import tornado.httpserver
import tornado.ioloop
import tornado.web
import sys

from tornado.netutil import bind_sockets
from multiprocessing import Process

import lpl_handler
from lpl_db import user_db, content_db, favorite_db
from lpl_const import config, secret

sys.path.append('/')


class LPLApplication(tornado.web.Application):
    def __init__(self, handlers, **settings):
        self.content_db = content_db.ContentDb()
        self.user_db = user_db.UserDb()
        self.favorite_db = favorite_db.FavoriteDb()
        self.salt = secret.salt
        tornado.web.Application.__init__(self, handlers, **settings)


# TODO:ハンドラーへのルーティングを整理したい。
application = LPLApplication([
    (r'/', lpl_handler.lpl_index_handler.LPLIndexHandler),
    (r'/?search', lpl_handler.lpl_index_handler.LPLIndexHandler),
    (r'/list.*', lpl_handler.lpl_list_handler.LPLListHandler),
    (r'/channel-videos.*', lpl_handler.lpl_chennel_videos_handler.LPLChannelVideosHandler),
    (r'/login.*', lpl_handler.lpl_login_handler.LPLLoginHandler),
    (r'/logout.*', lpl_handler.lpl_logout_handler.LPLLogoutHandler),
    (r'/create-account.*', lpl_handler.lpl_create_account_handler.LPLCreateAccountHandler),
    (r'/password-forgot.*', lpl_handler.lpl_password_forgot_handler.LPLPasswordForgotHandler),
    (r'/password-update.*', lpl_handler.lpl_password_update_handler.LPLPasswordUpdateHandler),
    (r'/good.*', lpl_handler.lpl_good_handler.LPLGoodHandler),
    (r'/api/favorite.*', lpl_handler.lpl_api_favorite_handler.LPLAPIFavoriteHandler),
    (r'/api/content.*', lpl_handler.lpl_api_content_handler.LPLAPIContentHandler),
    (r'/api/search-suggestion.*', lpl_handler.lpl_api_search_suggestion_handler.LPLAPISearchSuggestionHandler),
    (r'/null', lpl_handler.lpl_index_handler.LPLIndexHandler),
],
    template_path=os.path.join(os.getcwd(), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug=True,
    cookie_secret=secret.cookie_secret,
    xsrf_cookies=True
)
# def do_task():
#     print('タスク実行')
#
# def batch_run():
#     schedule.every().day.at("02:00").do(do_task)
#
#     while True:
#         schedule.run_pending()
#         time.sleep(1)


if __name__ == "__main__":
    server_port = config.port
    print("server start:" + str(server_port))
    # batch_runner = Process(target=batch_run)
    # batch_runner.start()

    if os.name == 'nt':
        print('on Windows')
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(server_port)
        tornado.ioloop.IOLoop.current().start()

    elif os.name == 'posix':
        print('on Mac or Linux')
        sockets = bind_sockets(server_port)
        tornado.process.fork_processes(0)


        async def post_fork_main():
            http_server = tornado.httpserver.HTTPServer(application)
            http_server.add_sockets(sockets)
            await asyncio.Event().wait()



        asyncio.run(post_fork_main())
