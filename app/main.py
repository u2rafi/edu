from fastapi import FastAPI, Depends, UploadFile, File, Form
from starlette.background import BackgroundTasks

from .utils import data_process_task

app = FastAPI(
    title="Education data API",
    description="Education data API service",
    version="1.0.0",
    docs_url="/"
)


@app.post('/api/v1/submit/')
async def data_submit(
        background_tasks: BackgroundTasks,
        year: int = Form(...),
        file: UploadFile = File(...),
        process_in_background: bool = Form(False)
) -> dict:
    """
    API that handles uploaded file from crawler

    Body:
    -------
    background_tasks: BackgroundTasks class for running job in background
    year: raking year in integer
    file: csv file containing ranking list
    process_in_background: (bool) if set `True` API task will run in background, default=False

    Responses:
    --------
    A Json object containing `status`, `background` and `count`
    status: Task status
    background: Is task running in background or not
    count: Number of data inserted/updated for non-background mode
    """
    if process_in_background:
        background_tasks.add_task(data_process_task, year, file)
        return {'status': 'accepted', 'background': process_in_background}
    else:
        dp = data_process_task(year, file)
        return {'total': dp.data_length, 'status': 'processed',
                'background': process_in_background}
