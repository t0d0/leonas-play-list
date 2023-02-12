import motor

from lpl_const import config

class BaseDb:

    def __init__(self):
        self.client = motor.motor_tornado.MotorClient(config.mongo_host, config.mongo_port)
        self.db = self.client.lpl_db
        self.fav_co = self.db.favorite_collection
        self.lpl_co = self.db.lpl_collection
        self.user_co = self.db.user_collection

    class DataFormat:
        def __getitem__(self, key):
            return self.__getattribute__(str(key))

