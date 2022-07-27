# coding:utf-8

import pymongo
from bson.objectid import ObjectId


# from functools import singledispatch
# from datetime import datetime
from lpl_const import constants


class ContentDb:
    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = self.client.lpl_db
        self.co = self.db.lpl_collection

    #   挿入
    def set_data(self, data):
        insert_data = {'title': data['title'], 'video_id': data['video_id'], 'time': data['time'], 'artist': ''}
        return self.co.insert_one(insert_data)

    #    更新
    def update_data(self, update_data):
        self.co.update_one({'_id': ObjectId(update_data['_id'])}, {'$set': {
            "title": update_data["title"],
            "video_id": update_data["video_id"],
            "time": update_data["time"],
            "artist": update_data["artist"],
        }})

    def get_data(self, search='', without_target=None, perfect=False):
        regex = constants.regex_keyword_any + search + constants.regex_keyword_any
        options = 'i'
        if perfect:
            regex = '^' + search + '$'
            options = ''
        if without_target is None:
            return (
                self.co.aggregate(
                    [
                        {
                            '$match': {
                                'title': {
                                    '$regex': regex,
                                    '$options': options
                                }
                            }
                        },
                        {'$sample': {'size': 20}},
                        {'$limit': 20}
                    ]
                )
            )

        without_object_id_list = []
        for target in without_target:
            without_object_id_list.append(ObjectId(target))
        return (
            self.co.aggregate(
                [
                    {
                        '$match': {
                            '$and': [
                                {'_id': {'$nin': without_object_id_list}},
                                {'title': {
                                    '$regex': regex,
                                    '$options': options}}
                            ]
                        },
                    },
                    {'$sample': {'size': 20}},
                    {'$limit': 20}
                ]
            )
        )

    def get_data_by_artist(self, artist, without_target=None):
        if without_target is None:
            without_target = []
        regex = '^' + artist + '$'
        options = ''
        if without_target is None:
            return (
                self.co.aggregate(
                    [
                        {
                            '$match': {
                                'artist': {
                                    '$regex': regex,
                                    '$options': options
                                }
                            }
                        },
                        {'$sample': {'size': 20}},
                        {'$limit': 20}
                    ]
                )
            )

        without_object_id_list = []
        for target in without_target:
            without_object_id_list.append(ObjectId(target))
        return (
            self.co.aggregate(
                [
                    {
                        '$match': {
                            '$and': [
                                {'_id': {'$nin': without_object_id_list}},
                                {'artist': {
                                    '$regex': regex,
                                    '$options': options}}
                            ]
                        },
                    },
                    {'$sample': {'size': 20}},
                    {'$limit': 20}
                ]
            )
        )

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
            '$match': {
                '$and': [
                    {
                        '_id': {'$nin': without_object_id_list},
                    }, {
                        '_id': {'$in': target_object_id_list}
                    },
                ]
            }
        }, {
            '$sample': {'size': 20}
        }]

        return self.co.aggregate(query)

    def get_data_by_id(self, target_id):
        return (
            self.co.aggregate(
                [
                    {
                        '$match': {
                            '_id': ObjectId(target_id)
                        }
                    }
                ]
            )
        )

    def get_title_list(self):
        return self.co.aggregate([{"$group": {"_id": "$title",
                                              "title": {"$first": '$title'},
                                              "artist": {"$first": '$artist'},
                                              "count": {"$sum": 1}
                                              }
                                   }

                                  ])

    def get_artist_list(self):
        return self.co.aggregate([{"$group": {"_id": "$artist",
                                              "artist": {"$first": '$artist'},
                                              "count": {"$sum": 1}
                                              }
                                   }

                                  ])

    def erase_data(self, target_id):
        self.co.delete_one({'_id': ObjectId(target_id)})

    def increment_good(self, target_id):
        self.co.update({'_id': ObjectId(target_id)}, {'$inc': {'good': 1}})
