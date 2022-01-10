## Education dp exercise
A python programming exercise, processing education dataset

#### Requirements
* Python3.7
* FastAPI

### Installation, run and testing

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
```

CURL

```
curl -X 'POST' \
  'http://0.0.0.0:8000/api/v1/submit/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'year=2018' \
  -F 'file=@data-2018.txt;type=text/plain'
```

Python requests

```
import requests

url = "http://0.0.0.0:8000/api/v1/submit/"

payload={'year': '2018'}
files=[
  ('file',('file',open('/path/to/file','rb'),'application/octet-stream'))
]
headers = {
  'accept': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
```