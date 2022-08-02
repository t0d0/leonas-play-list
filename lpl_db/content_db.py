#!/usr/bin/python
# -*- coding: utf-8 -*-
"""コンテンツDBへのアクセス用"""
from typing import Any

import pymongo
from bson.objectid import ObjectId

from lpl_const import constants
from lpl_db.base_db import BaseDb


class ContentDb(BaseDb):
    """
    コンテンツDB操作用クラス
    """

    class DataFormat:
        """
        データ更新用のフォーマット用クラス
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

        def __init__(self, title: str = "", video_id: str = "", time: int = 0, artist: str = "", _id: str = ""):
            self.title = title
            self.video_id = video_id
            self.time = time
            self.artist = artist
            self._id = _id

        def __getitem__(self, key):
            return self.__getattribute__(key)

    async def set_data(self, data: DataFormat):
        """新規コンテンツの挿入

        Args:
            data:新規挿入データ

        Returns:
            挿入結果

        Examples:
            content_db.set_data({"title":"hoge","video_id":"xxxxx","time":999})

        """
        insert_data = {"title": data["title"], "video_id": data["video_id"], "time": data["time"], "artist": ""}
        result = await self.lpl_co.insert_one(insert_data)
        return result

    #    更新
    async def update_data(self, update_data: DataFormat) -> dict[str, Any]:
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

    def get_data(self, search: str = "", without_target: list[str] = None, perfect: bool = False):
        regex = constants.regex_keyword_any + search + constants.regex_keyword_any
        options = "i"
        if perfect:
            regex = "^" + search + "$"
            options = ""
        if without_target is None:
            return (
                self.lpl_co.aggregate(
                    [
                        {
                            "$match": {
                                "title": {
                                    "$regex": regex,
                                    "$options": options
                                }
                            }
                        },
                        {"$sample": {"size": 20}},
                        {"$limit": 20}
                    ]
                )
            ).to_list(None)

        without_object_id_list = []
        for target in without_target:
            without_object_id_list.append(ObjectId(target))
        return (
            self.lpl_co.aggregate(
                [
                    {
                        "$match": {
                            "$and": [
                                {"_id": {"$nin": without_object_id_list}},
                                {"title": {
                                    "$regex": regex,
                                    "$options": options}}
                            ]
                        },
                    },
                    {"$sample": {"size": 20}},
                    {"$limit": 20}
                ]
            )
        ).to_list(None)

    def get_data_by_artist(self, artist, without_target=None):
        if without_target is None:
            without_target = []
        regex = "^" + artist + "$"
        options = ""
        if without_target is None:
            return (
                self.lpl_co.aggregate(
                    [
                        {
                            "$match": {
                                "artist": {
                                    "$regex": regex,
                                    "$options": options
                                }
                            }
                        },
                        {"$sample": {"size": 20}},
                        {"$limit": 20}
                    ]
                )
            ).to_list(None)

        without_object_id_list = []
        for target in without_target:
            without_object_id_list.append(ObjectId(target))
        return (
            self.lpl_co.aggregate(
                [
                    {
                        "$match": {
                            "$and": [
                                {"_id": {"$nin": without_object_id_list}},
                                {"artist": {
                                    "$regex": regex,
                                    "$options": options}}
                            ]
                        },
                    },
                    {"$sample": {"size": 20}},
                    {"$limit": 20}
                ]
            )
        ).to_list(None)

    def get_data_by_ids(self, target_ids=None, without_target=None):
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

        query = [{
            "$match": {
                "$and": [
                    {
                        "_id": {"$nin": without_object_id_list},
                    }, {
                        "_id": {"$in": target_object_id_list}
                    },
                ]
            }
        }, {
            "$sample": {"size": 20}
        }]

        return self.lpl_co.aggregate(query).to_list(None)

    def get_data_by_id(self, target_id):
        result = self.lpl_co.aggregate(
            [
                {
                    "$match": {
                        "_id": ObjectId(target_id)
                    }
                }
            ]
        ).to_list(None)
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
