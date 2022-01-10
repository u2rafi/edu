from fastapi.testclient import TestClient
import os
from edu.app.main import app

client = TestClient(app)


def test_data_api():
    body = {
        'year': 2018
    }
    file = os.path.join(os.getcwd(), 'data/data-2018-test.txt')
    response = client.post('/api/v1/submit/', data=body, files={'file': open(file, 'rb')})
    assert response.status_code == 200
