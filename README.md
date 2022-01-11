## Education dp exercise
A python programming exercise, processing education dataset

#### Requirements
* Python == 3.9
* FastAPI

### Installation, run and testing


#### Setup .env file
copy `.env.example` to `.env` in the project root directory and update contents

```
MONGO_DSN=<mongo db host dsn> (mongodb://localhost:27017)
DUCK_DUCK_GO_APT_ENDPOINT=https://api.duckduckgo.com/
```

#### Run locally 
```
cd edu
uvicorn app.main:app --workers 3 --timeout-keep-alive 120 --host 0.0.0.0 --port 8000
```

#### Docker and docker compose

```
# docker 
docker build -t edu .
docker run -p 8000:8000 edu:latest

# docker compose
docker-compose up -d --build
```

#### Kubernetes
```
kubectl apply -f k8s-deployment.yml -n default
```

### Testing

Test cases are in `/edu/tests` directory

#### Test using pytest

```
pytest tests
```

#### Test using pytest-cov
Test coverage 
```
pytest --cov=edu tests/
```

# API
After running application, visit `http://0.0.0.0:8000` to find swagger api doc.

### Submit data 

`POST /api/v1/submit/`

Body 

```
multipart/form-data

year: Year of university ranking
file: .txt file containing university ranking data
process_in_background: true/false for running task in background
```

CURL

```
curl -X 'POST' \
  'http://0.0.0.0:8000/api/v1/submit/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'year=2018' \
  -F 'file=@data-2018-test.txt;type=text/plain' \
  -F 'process_in_background=true'
```

Python requests

```
import requests

url = "http://0.0.0.0:8000/api/v1/submit/"

payload = {
    'year': '2018',
    'process_in_background': 'true'
}
files = [
  ('file',('file',open('/path/to/file','rb'),'application/octet-stream'))
]
headers = {
  'accept': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
```

# Demo
A demo app has been deployed in heroku docker and can be accessed using this link

Note : For this demo, MongoDB has been deployed in digitalocean

[https://fierce-mountain-82505.herokuapp.com/](https://fierce-mountain-82505.herokuapp.com/)