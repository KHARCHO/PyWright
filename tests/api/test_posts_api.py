"""Demo API tests against jsonplaceholder - use as a pattern for real endpoints."""
import pytest
from qase.pytest import qase

from api.api_client import ApiClient

pytestmark = pytest.mark.api


@pytest.mark.smoke
@qase.title("Get post returns 200 with requested id")
def test_get_post(api: ApiClient):
    response = api.get("/posts/1")

    assert response.status == 200
    assert response.json()["id"] == 1


@pytest.mark.regression
@qase.title("Create post returns 201 and echoes payload")
def test_create_post(api: ApiClient):
    payload = {"title": "PyWright", "body": "template check", "userId": 1}

    response = api.post("/posts", data=payload)

    assert response.status == 201
    assert payload.items() <= response.json().items()
