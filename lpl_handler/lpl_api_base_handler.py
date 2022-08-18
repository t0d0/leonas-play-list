# coding:utf-8
import json
from typing import Optional, Any

import tornado
from tornado import httputil
from tornado.escape import json_decode
from tornado.routing import _RuleList


class LPLAPIBaseHandler(tornado.web.RequestHandler):
    SUPPORTED_METHODS = tornado.web.RequestHandler.SUPPORTED_METHODS + ('QUERY',)
    args = {}

    # def initialize(self) -> None:
    #     self.args = None

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
