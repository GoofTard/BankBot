import os
import pymongo
from datetime import datetime


class DatabaseConnection(object):
    users = None
    db = None
    dbClient = None
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            print('Creating new instance')
            cls._instance = cls.__new__(cls)

            cls.dbClient = pymongo.MongoClient(os.environ.get('MONGO_KEY'))

            if not 'admin' in cls.dbClient.list_database_names():
                raise Exception("DB Does'nt Esists")

            print("Successfully Connected to DB!")

            cls.db = cls.dbClient["admin"]
            cls.users = cls.db["users"]

        return cls._instance

    def getUser(self, userId) -> dict:
        if self.users.count_documents({"id": userId}) == 0:
            raise Exception("No Such User Exception")

        return self.users.find_one({"id": userId})

    def getLastMonth(self):
        return self.db["last_month"].find_one()["date"]

    def updateLastMonth(self):
        self.db["last_month"].update_one(
            {},
            {
                "$set": {
                    "date": datetime(datetime.now().year, datetime.now().month, 1)
                }
            }
        )

    def updateUser(self, query: dict, id: str) -> bool:
        try:
            self.users.update_one(
                {"id": id},
                query
            )
            return True
        except:
            return False

    def updateUsers(self, query: dict) -> bool:
        try:
            self.users.update_many(
                {},
                query
            )
            return True
        except:
            return False

    def registerUser(self, userId: str) -> bool:
        try:
            self.users.insert_one({
                "id": userId,
                "data": {
                    "percentages": {},
                    "totals": {},
                    "total": 0
                },
                "usages": {
                    "total": 0,
                    "transactions": []
                },
                "limits": {},
                "locks": []
            })

            return True
        except:
            return False

    def resetTestUser(self):
        try:
            self.users.delete_one({"id": "TEST"})
            self.registerUser("TEST")
            return True
        except:
            return False

    def addLock(self, userId: str, category: str):
        try:
            self.users.update_one(
                {"id": userId},
                {
                    "$addToSet": {
                        "locks": category
                    }
                }
            )
            return True
        except:
            return False

    def remLock(self, userId: str, category: str):
        try:
            self.users.update_one(
                {"id": userId},
                {
                    "$pull": {
                        "locks": category
                    }
                }
            )
            return True
        except:
            return False

    def addLimit(self, userId: str, category: str, limit: float):
        try:
            self.users.update_one(
                {"id": userId},
                {
                    "set": {
                        f"limits.{category}": limit
                    }
                }
            )
            return True
        except:
            return False

    def remLimit(self, userId: str, category: str):
        try:
            self.users.update_one(
                {"id": userId},
                {
                    "unset": {
                        f"limits.{category}": ""
                    }
                }
            )
            return True
        except:
            return False
