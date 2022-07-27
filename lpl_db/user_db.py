# coding:utf-8

import pymongo


# from functools import singledispatch
# from datetime import datetime

class UserDb:
    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = self.client.lpl_db
        self.co = self.db.user_collection

    def set_data(self, data):
        insert_data = {'e-mail': data['e-mail'], '_id': data['e-mail'], 'password': data['password']}
        return self.co.insert_one(insert_data)

    def get_data(self, user='', password=''):
        return (
            self.co.find_one({
                "_id": user,
                "password": password
            })
        )

    def get_data_by_id(self, target_id):
        return (
            self.co.aggregate(
                [
                    {
                        '$match': {
                            '_id': target_id
                        }
                    }
                ]
            )
        )

    def erase_data(self, target_id):
        self.co.delete_one({'_id': target_id})
