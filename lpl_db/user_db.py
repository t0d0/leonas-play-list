# coding:utf-8
from lpl_db.base_db import BaseDb


class UserDb(BaseDb):
    
    def set_data(self, data):
        insert_data = {'e-mail': data['e-mail'], '_id': data['e-mail'], 'password': data['password']}
        return self.user_co.insert_one(insert_data)

    def get_data(self, user='', password=''):
        return (
            self.user_co.find_one({
                "_id": user,
                "password": password
            })
        )

    def get_data_by_id(self, target_id):
        return (
            self.user_co.aggregate(
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
        self.user_co.delete_one({'_id': target_id})
