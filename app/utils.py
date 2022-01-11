from fastapi import UploadFile
from .contrib import FileHandler, DataProcess
from .mongo import MongoStorage


def data_process_task(year: int, file: UploadFile) -> DataProcess:
    """
    Data process takes file object and pass it to FileHandler for processing with DataProcess
    Parameters
    ----------
    year: year in int for university ranking
    file: UploadFile file containing university ranking list from API payload

    Returns
    ----------
    DataProcess object
    """
    # load file using file handler
    fh = FileHandler(file.file)
    db = MongoStorage()  # mongo db
    dp = DataProcess(fh, db, year)  # data processing
    dp.run()
    return dp
