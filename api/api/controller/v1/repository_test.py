import pytest

from api.util import uuidgen
from api.view.v1 import api_bp

API_URL_PREFIX = api_bp.url_prefix
API_REQUEST_HEADERS = {"Content-Type": "application/json"}


@pytest.mark.order(1000)
def test_get_repositories_apiv1(client):
    response = client.get(
        f"{API_URL_PREFIX}/repositories",
        headers=API_REQUEST_HEADERS,
    )
    result = response.get_json()
    assert response.status_code == 200
    assert result["status"]["code"] == 100
    assert result["status"]["message"] == "OK."
    assert len(result["output"]) == 1


@pytest.mark.parametrize(
    ("repository_id", "status", "code"),
    (
        ("random", 404, 105),
        ("storage:test", 200, 100),
    ),
)
@pytest.mark.order(1000)
def test_get_repository_apiv1(storage, client, repository_id, status, code):
    if repository_id == "random":
        repository_id = uuidgen()
    if repository_id.startswith("storage:") is True:
        repository_id = storage.get(repository_id.split(":")[1])
    response = client.get(
        f"{API_URL_PREFIX}/repositories/{repository_id}",
        headers=API_REQUEST_HEADERS,
    )
    result = response.get_json()
    assert response.status_code == status
    assert result["status"]["code"] == code


@pytest.mark.parametrize(
    ("data", "status", "code"),
    (
        ({}, 400, 104),
        ({"bad": True}, 400, 104),
        ({"url": "http://test.com/test.git", "bad": True}, 400, 104),
        ({"url": False}, 400, 104),
        ({"url": "http://test.com/test.git"}, 201, 100),
        ({"url": "http://test.com/test.git"}, 201, 100),
    ),
)
@pytest.mark.order(1001)
def test_create_repository_apiv1(storage, client, data, status, code):
    response = client.post(
        f"{API_URL_PREFIX}/repositories",
        headers=API_REQUEST_HEADERS,
        json=data,
    )
    result = response.get_json()
    assert response.status_code == status
    assert result["status"]["code"] == code
    if response.status_code == 201:
        assert result["output"]["status"] == "NEW"
        assert result["output"]["last_update_at"] is None
        assert result["output"]["owner"] == "TBC"
        if hasattr(storage, "temp1") is False:
            storage.set("temp1", result["output"]["id"])
        else:
            storage.set("temp2", result["output"]["id"])


@pytest.mark.parametrize(
    ("repository_id", "data", "status", "code"),
    (
        ("random", {}, 404, 105),
        ("storage:temp1", {}, 400, 104),
        ("storage:temp1", {"status": ""}, 400, 107),
        ("storage:temp1", {"bad": True}, 400, 104),
        ("storage:temp1", {"status": "ACCEPTED", "bad": True}, 400, 104),
        ("storage:temp2", {"status": "ACCEPTED"}, 200, 100),
    ),
)
@pytest.mark.order(1002)
def test_update_repository_apiv1(storage, client, repository_id, data, status, code):
    if repository_id == "random":
        repository_id = uuidgen()
    if repository_id.startswith("storage:") is True:
        repository_id = storage.get(repository_id.split(":")[1])
    response = client.patch(
        f"{API_URL_PREFIX}/repositories/{repository_id}",
        headers=API_REQUEST_HEADERS,
        json=data,
    )
    result = response.get_json()
    assert response.status_code == status
    assert result["status"]["code"] == code


@pytest.mark.parametrize(
    ("repository_id", "status", "code"),
    (
        ("random", 404, 105),
        ("storage:temp1", 200, 100),
        ("storage:temp2", 412, 106),
    ),
)
@pytest.mark.order(1003)
def test_delete_repository_apiv1(storage, client, repository_id, status, code):
    if repository_id == "random":
        repository_id = uuidgen()
    if repository_id.startswith("storage:") is True:
        repository_id = storage.get(repository_id.split(":")[1])
    response = client.delete(
        f"{API_URL_PREFIX}/repositories/{repository_id}",
        headers=API_REQUEST_HEADERS,
    )
    result = response.get_json()
    assert response.status_code == status
    assert result["status"]["code"] == code
