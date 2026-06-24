def test_daily_activity(
    client,
    header_token,
    daily_activity
):

    response = client.get(
        "/users/daily-activity",
        headers=header_token
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0

    assert data[0]["problems_solved"] == 8


def test_tags(
    client,
    header_token,
    tag_performance
):

    response = client.get(
        "/users/tags",
        headers=header_token
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0

    assert data[0]["tag_name"] == "graphs"

    assert data[0]["success_rate"] == 70.0


def test_weakest_tags(
    client,
    header_token,
    tag_performance
):

    response = client.get(
        "/users/tags/weakest",
        headers=header_token
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0

    assert data[0] == "graphs"

def test_recommendations(
    client,
    header_token,
    recommendation
):

    response = client.get(
        "/users/recommendations",
        headers=header_token
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0

    assert (
        data[0]["recommendation_type"]
        == "weak_tag_improvement"
    )


    
def test_contests(
    client,
    header_token,
    contest_performance
):

    response = client.get(
        "/users/contests",
        headers=header_token
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0



def test_contests_unauthorized(client):

    response = client.get("/users/contests")

    assert response.status_code == 401
def test_recommendations_unauthorized(client):

    response = client.get("/users/recommendations")

    assert response.status_code == 401
def test_daily_activity_unauthorized(client):

    response = client.get("/users/daily-activity")

    assert response.status_code == 401
def test_tags_unauthorized(client):

    response = client.get("/users/tags")

    assert response.status_code == 401
def test_tags_weakest_unauthorized(client):

    response = client.get("/users/tags/weakest")

    assert response.status_code == 401

