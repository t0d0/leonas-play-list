# coding:utf-8


from lpl_db.base_db import BaseDb


class FavoriteDb(BaseDb):

    def set_data(self, user='', favorite_id=''):
        insert_data = {'e-mail': user, 'favorites': []}
        set_target = self.get_data(user)
        if set_target is None:
            #            新規作成
            insert_data['favorites'] = [favorite_id]
            self.fav_co.insert_one(insert_data)
        else:
            #            更新
            insert_data = set_target
            insert_data['favorites'].append(favorite_id)
            insert_data['favorites'] = list(set(insert_data['favorites']))
            self.fav_co.update_one({'e-mail': insert_data['e-mail']}, {'$set': insert_data})
        return insert_data

    def remove_data(self, user='', favorite_id=''):
        set_target = self.get_data(user)
        set_target['favorites'].remove(favorite_id)
        self.fav_co.update_one({'e-mail': set_target['e-mail']}, {'$set': set_target})

    def get_data(self, user=''):
        return (
            self.fav_co.find_one({
                "e-mail": user
            })
        )

    def get_data_by_id(self, target_id):
        return (
            self.fav_co.aggregate(
                [
                    {
                        '$match': {
                            '_id': target_id
                        }
                    }
                ]
            )
        ).to_list(None)

    def erase_data(self, target_id):
        self.fav_co.delete_one({'_id': target_id})
