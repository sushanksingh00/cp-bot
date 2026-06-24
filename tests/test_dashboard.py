from crud import delete_user

def test_dashboard_unauthorized(client):

    response = client.get("/users/dashboard")

    assert response.status_code == 401

def test_dashboard_independent(
    client,
    header_token,
    dashboard_data
):

    response = client.get(
        "/users/dashboard",
        headers=header_token
    )

    assert response.status_code == 200

    data = response.json()

    assert data