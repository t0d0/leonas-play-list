# coding:utf-8

import tornado
from tornado.escape import json_decode


class LPLAPIBaseHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = tornado.web.RequestHandler.SUPPORTED_METHODS + ('QUERY',)
    args = {}

    def prepare(self):
        if self.request.headers['Content-Type'] == 'application/json':
            self.args = json_decode(self.request.body)
            print("prepare")
            print(self.args)

    def get_argument(self,name:str,default:str=''):
        # print('default='+default)
        if name in self.args.keys():
            if self.args[name] is not None:
                return self.args[name]
            else:
                return default
        else:
            return default
