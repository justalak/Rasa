from peewee import *


class Database:
    DB = None

    def __init__(self):
        """ Virtually private constructor. """
        if Database.DB is not None:
            raise Exception("This class is a singleton!")
        else:
            Database.DB = MySQLDatabase('stocks', user='root', password='mysql',
                                                 host='localhost', port=3306)

    @staticmethod
    def getDB():
        if Database.DB is None:
            Database()
        return Database.DB

