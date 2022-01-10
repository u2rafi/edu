from edu.app.mongo import MongoStorage
import os


def test_mongo_storage():
    db = MongoStorage()
    db.collection('test').update_or_insert(select={'ssn': '111111'}, first_name='John', last_name='Doe', ssn='111111')
    user = db.collection('test').get(ssn='111111')
    assert user.get('first_name') == 'John'
