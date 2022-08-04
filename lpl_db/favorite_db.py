# coding:utf-8


from lpl_db.base_db import BaseDb


class FavoriteDb(BaseDb):
    class UpdateFavoriteDataFormat(BaseDb.DataFormat):
        """
        データ更新用のフォーマット用クラス
        """
        user: str
        """ユーザーID"""
        favorite_id: str
        """コンテンツID"""

        def __init__(self, user: str = "", favorite_id: str = ""):
            self.user = user
            self.favorite_id = favorite_id

    class FindFavoriteDataFormat(BaseDb.DataFormat):
        """
        データ取得用のフォーマット用クラス
        """
        user: str
        """ユーザーID"""
        favorites: str
        """コンテンツIDの"""

        def __init__(self, user: str = "", favorites: list[str] = []):
            self.user = user
            self.favorites = favorites

    async def set_data(self, user='', favorite_id=''):
        insert_data = {'e-mail': user, 'favorites': []}
        set_target = await self.get_data(user)
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

    async def remove_data(self, user='', favorite_id=''):
        set_target = await self.get_data(user)
        set_target['favorites'].remove(favorite_id)
        self.fav_co.update_one({'e-mail': set_target['e-mail']}, {'$set': set_target})

    def get_data(self, user=''):
        # print(user)
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
