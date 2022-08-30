#!/usr/bin/python
# -*- coding: utf-8 -*-
"""コンテンツDBへのアクセス用"""
from typing import Any

from bson.objectid import ObjectId

from lpl_const import constants
from lpl_db.base_db import BaseDb


class ContentDb(BaseDb):
    """
    コンテンツDB操作用クラス
    """

    class ContentDataFormat(BaseDb.DataFormat):
        """
        コンテンツデータ取得/更新用のフォーマット用クラス
        """
        title: str
        """曲名"""
        video_id: str
        """動画のID"""
        time: int
        """開始時間"""
        artist: str
        """アーティスト情報"""
        _id: str
        """コンテンツID"""
        published_at: str
        """投稿日"""

        def __init__(self, title: str = "", video_id: str = "", time: int = 0, artist: str = "", _id: str = "",
                     published_at: str = ""):
            self.title = title
            self.video_id = video_id
            self.time = time
            self.artist = artist
            self._id = _id
            self.published_at = published_at

    async def set_data(self, data: ContentDataFormat):
        """新規コンテンツの挿入

        Args:
            data:新規挿入データ

        Returns:
            挿入結果

        Examples:
            content_db.set_data({"title":"song_title","video_id":"xxxxx","time":999})

        """
        insert_data = {
            "title": data["title"],
            "video_id": data["video_id"],
            "time": data["time"],
            "artist": "",
            "published_at" : data["published_at"]
        }
        result = await self.lpl_co.insert_one(insert_data)
        return result

    #    更新
    async def update_data(self, update_data: ContentDataFormat) -> dict[str, Any]:
        await self.lpl_co.update_one({
            "_id": ObjectId(update_data["_id"])},
            {"$set": {
                "title": update_data["title"],
                "video_id": update_data["video_id"],
                "time": update_data["time"],
                "artist": update_data["artist"],
            }})
        result = await self.get_data_by_id(update_data["_id"])
        return list(result)

    async def get_data(self, search: str = "", without_target: list[str] = None, perfect: bool = False):
        regex = constants.regex_keyword_any + '\Q' + search + '\E' + constants.regex_keyword_any
        options = "i"
        if perfect:
            regex = "^" + '\Q' + search + '\E' + "$"
            options = ""

        if without_target is None:
            detail_query = {
                "$or": [
                    {"title": {
                        "$regex": regex,
                        "$options": options
                    }},
                    {"artist": {
                        "$regex": regex,
                        "$options": options
                    }}
                ]}
        else:
            without_object_id_list = []
            for target in without_target:
                without_object_id_list.append(ObjectId(target))
            detail_query = {
                "$and": [
                    {"_id": {"$nin": without_object_id_list}},
                    {"$or": [
                        {"title": {
                            "$regex": regex,
                            "$options": options
                        }},
                        {"artist": {
                            "$regex": regex,
                            "$options": options
                        }}
                    ]}]}

        query = self.__build_get_content_query(detail_query)
        print(type(query))
        query_result = self.lpl_co.aggregate(query)
        result = await self.__result_to_model_list(query_result)
        return result

    async def get_data_by_artist(self, artist, without_target=None):
        regex = "^\Q" + artist + "\E$"
        options = ""
        if without_target is None:
            detail_query = {
                "artist": {
                    "$regex": regex,
                    "$options": options
                }}
        else:
            without_target = []
            without_object_id_list = []
            for target in without_target:
                without_object_id_list.append(ObjectId(target))
            detail_query = {
                "$and": [
                    {"_id": {"$nin": without_object_id_list}},
                    {"artist": {
                        "$regex": regex,
                        "$options": options
                    }}]}

        query = self.__build_get_content_query(detail_query)

        query_result = self.lpl_co.aggregate(query)
        result = await self.__result_to_model_list(query_result)
        return result

    async def get_data_by_ids(self, target_ids=None, without_target=None):
        if without_target is None:
            without_target = []
        if target_ids is None:
            target_ids = []
        without_object_id_list = []
        for target in without_target:
            without_object_id_list.append(ObjectId(target))
        target_object_id_list = []
        for target in target_ids:
            target_object_id_list.append(ObjectId(target))

        detail_query = {
            "$and": [
                {"_id": {"$nin": without_object_id_list}},
                {"_id": {"$in": target_object_id_list}}
            ]}

        query = self.__build_get_content_query(detail_query)
        query_result = self.lpl_co.aggregate(query)
        result = await self.__result_to_model_list(query_result)
        return result

    async def get_data_by_id(self, target_id):

        detail_query = {"_id": ObjectId(target_id)}

        query = self.__build_get_content_query(detail_query)
        query_result = self.lpl_co.aggregate(query)
        result = await self.__result_to_model_list(query_result)
        return result

    def get_title_list(self):
        return self.lpl_co.aggregate([{"$group": {"_id": "$title",
                                                  "title": {"$first": "$title"},
                                                  "artist": {"$first": "$artist"},
                                                  "count": {"$sum": 1}
                                                  }
                                       }

                                      ]).to_list(None)

    def get_artist_list(self):
        return self.lpl_co.aggregate([{"$group": {"_id": "$artist",
                                                  "artist": {"$first": "$artist"},
                                                  "count": {"$sum": 1}
                                                  }
                                       }

                                      ]).to_list(None)

    def erase_data(self, target_id):
        self.lpl_co.delete_one({"_id": ObjectId(target_id)})

    def increment_good(self, target_id):
        self.lpl_co.update({"_id": ObjectId(target_id)}, {"$inc": {"good": 1}})

    def __build_get_content_query(self, detail_query):
        query = [
            {"$match": detail_query},
            {"$sample": {"size": 20}},
            {"$limit": 20}
        ]
        return query

    async def __result_to_model_list(self, result):
        model_list = []
        async for data in result:
            model = self.ContentDataFormat(
                data["title"],
                data["video_id"],
                data["time"],
                data["artist"],
                str(data["_id"]),
                data["published_at"] if "published_at" in data else None
            )
            model_list.append(model.__dict__)

        return model_list
