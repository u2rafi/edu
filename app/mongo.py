from typing import Any
from pymongo import MongoClient
from .config import settings


class MongoStorage(object):
    """
    Simply stores data into mongodb

    Usage
    -------
    > db = MongoStorage()
    > db.collection('test').update_or_insert(select={key: value}, **data)
    """

    def __init__(self):
        self.dsn = settings.MONGO_DSN
        self.database = 'edu'
        self._collections = 'rank', 'info'
        self._collection = None

    def __call__(self, *args, **kwargs):
        for col in self._collections:
            setattr(self, col, self.collection(col))

    @property
    def client(self):
        return MongoClient(self.dsn)

    def get_database(self) -> Any:
        return self.client[self.database]

    def collection(self, name: str) -> Any:
        self._collection = self.get_database()[name]
        return self

    def insert(self, **kwargs) -> None:
        self._collection.insert_one(kwargs)
        return None

    def update_or_insert(self, select: dict, **kwargs) -> Any:
        """
        Create mongo document by the given kwargs updates if matched with `select dictionary`

        Parameters
        ----------
        defaults: query to select object
        kwargs: Updated object

        Returns
        -------
        tuple consisting created=True/False and replace_one response
        """
        if self._collection is None:
            raise AssertionError('Must provide collection name in storage object `cls.collection("name")`')
        result = self._collection.replace_one(select, kwargs, True)
        return result.matched_count == 0, result

    def get(self, **kwargs) -> Any:
        if self._collection is None:
            raise AssertionError('Must provide collection name in storage object `cls.collection("name")`')
        return self._collection.find_one(kwargs)
