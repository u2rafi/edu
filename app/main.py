from fastapi import FastAPI, Depends, UploadFile, File, Form

from .contrib import FileHandler, DataProcess
from .models import DataInpModel
from .mongo import MongoStorage

app = FastAPI(
    title="Education data API",
    description="Education data API service",
    version="1.0.0",
    docs_url="/"
)


@app.post('/api/v1/submit/')
async def data_submit(year: int = Form(...), file: UploadFile = File(...)):
    # load file using file handler
    fh = FileHandler(file.file)
    db = MongoStorage()  # mongo db
    dp = DataProcess(fh, db, year)  # data processing
    dp.run()
    return {'success': dp.success, 'total': dp.data_length}
