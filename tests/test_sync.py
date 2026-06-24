
from crud import delete_user


def test_sync(client, header_token):

    try:
        response = client.post(
            "/sync/codeforces",
            json={
                "platform" : "codeforces",
                "handle" : "Um_nik"
            },
            headers=header_token
        )

        assert response.status_code == 200

        task_id = response.json()["task_id"]

        status = check_status(client, task_id, header_token)

        assert status == "SUCCESS"


    finally:
        delete_user("codeforces", "Um_nik")



import time
import pytest

def check_status(client, task_id, header_token):
    for _ in range(60):

        response = client.get(
            f"/sync/status/{task_id}",
            headers=header_token
        )

        status = response.json()["state"]

        if status == "SUCCESS":
            return status

        if status == "FAILURE":
            pytest.fail("Sync task failed")

        time.sleep(1)

    else:
        pytest.fail("Sync task timed out")

def test_dashboard(client, synced_header_token):

    dashboard_response = client.get(
        "/users/dashboard",
        headers=synced_header_token
    )

    assert dashboard_response.status_code == 200

    data = dashboard_response.json()

    assert "user" in data
    assert "weakest_tags" in data
    assert "recommendations" in data
    assert "recent_activity" in data
    assert "total_contests" in data
    assert "total_questions" in data
    assert "total_days_active" in data

    
