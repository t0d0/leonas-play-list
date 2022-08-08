# coding:utf-8
import tornado


class LPLIndexBaseHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = tornado.web.RequestHandler.SUPPORTED_METHODS + ('QUERY',)

