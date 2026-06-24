def test_recommendations(
    client,
    header_token,
    dashboard_data
):

    response = client.get(
        "/users/recommendations",
        headers=header_token
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0