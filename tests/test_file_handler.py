from edu.app.contrib import FileHandler
import os

def test_file_handler():
    file = os.path.join(os.getcwd(), 'data/data-2018-test.txt')
    fh = FileHandler(file)
    keys, records = fh.read()
    assert len(records) > 0
