from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# generic test
def test_get_base_endpoint():
    response = client.get('/')
    assert response.status_code == 200


def test_urls():
    response = client.get('/urls')
    assert response.status_code == 422
