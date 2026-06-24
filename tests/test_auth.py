
def test_register_success(client, user_data):

    data = user_data

    response = client.post(
        "/auth/register",
        json=data
    )

    assert response.status_code == 200

def test_register_duplicate(client, registered_user):

    data={
        "username" : registered_user.username,
        "email": registered_user.email,
        "password" : "12345678"
    }

    response = client.post("/auth/register", json=data)

    assert response.status_code == 401


def test_login_failed_name(client, registered_user):

    data= {
        "username":registered_user.username+"abc",
        "password": "12345678"
    }

    response = client.post("/auth/login", json=data)

    assert response.status_code == 401

def test_login_failed_password(client, registered_user):

    data= {
        "username":registered_user.username,
        "password": "12345678" + "123"
    }

    response = client.post("/auth/login", json=data)

    assert response.status_code == 401


def test_login_successfull(client, registered_user):

    data= {
        "username": registered_user.username,
        "password": "12345678"
    }

    response = client.post("/auth/login", json=data)
    

    assert response.status_code == 200
    assert response.json()["token"] 
