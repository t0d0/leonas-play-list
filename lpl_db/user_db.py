# coding:utf-8
from typing import Optional

import pymongo
from pymongo.errors import DuplicateKeyError

from lpl_db.base_db import BaseDb


class UserDb(BaseDb):
    '''
    ユーザDB操作用クラス
    '''

    class DataFormat:
        '''
        データ更新用のフォーマット用クラス
        '''
        e_mail: str
        '''メールアドレス'''
        password: str
        '''動画のID'''
        _id: str
        '''ユーザID（基本的にメールアドレス）'''

        def __init__(self, e_mail: str, password: str, _id: str):
            """DataFormatのコンストラクタ

            Args:
                e_mail (): メールアドレス
                password (): ハッシュ済みのパスワード
                _id (): ユーザID（基本的にメールアドレス）
            """
            self.e_mail = e_mail
            self.password = password
            self._id = _id

        def __getitem__(self, key):
            return self.__getattribute__(key)

    async def set_data(self, data: DataFormat) -> Optional[pymongo.results.InsertOneResult]:
        """新規ユーザの挿入

        Args:
            data (): 新規挿入データ

        Returns:挿入結果(pymongo.results.InsertOneResult)
        ユーザ重複の場合はNoneを返します。

        """
        try:
            insert_data = {'e-mail': data['e_mail'], '_id': data['_id'], 'password': data['password']}
            result: pymongo.results.InsertOneResult = await self.user_co.insert_one(insert_data)
        except DuplicateKeyError:
            print("ユーザ重複エラー")
            result = None

        return result

    async def get_data(self, user: str = '', password: str = '') -> Optional[pymongo.typings._DocumentType]:
        """

        Args:
            user ():ユーザーID
            password (): ハッシュ済みのパスワード

        Returns:

        """
        result: Optional[pymongo.typings._DocumentType] = await self.user_co.find_one({
            "_id": user,
            "password": password
        })
        return result

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
