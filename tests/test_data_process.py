from edu.app.contrib import FileHandler, DataProcess
from edu.app.mongo import MongoStorage
import os


def test_data_process():
    file = os.path.join(os.getcwd(), 'data/data-2018-test.txt')
    fh = FileHandler(file)
    db = MongoStorage()
    dp = DataProcess(fh, db, 2018)
    dp.run()
    assert dp.data_length > 0
