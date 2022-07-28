import motor


class BaseDb:

    def __init__(self):
        self.client = motor.motor_tornado.MotorClient('localhost', 27017)
        self.db = self.client.lpl_db
        self.fav_co = self.db.favorite_collection
        self.lpl_co = self.db.lpl_collection
        self.user_co = self.db.user_collection
