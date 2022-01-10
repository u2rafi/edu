FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
WORKDIR /code
COPY . /code
RUN pip install -r requirements.txt
EXPOSE 8000