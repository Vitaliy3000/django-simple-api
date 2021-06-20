from data import *


def test_authenticate(user_client):
    user_client.authenticate(email=USER_EMAIL, password=USER_PASSWORD)
    assert user_client.is_authenticated is True


def test_resource_flow(user_client):
    user_client.authenticate(email=USER_EMAIL, password=USER_PASSWORD)

    # creating resource
    response = user_client.create_resource(USER_RESOURCE_NAME)
    assert response.status_code == 201, response.content
    resource_id = response.json()["id"]

    # getting resources
    response = user_client.list_resources()
    assert response.status_code == 200, response.content
    assert len(response.json()) == 1, response.json()

    # attemt create duplicate resource
    response = user_client.create_resource(USER_RESOURCE_NAME)
    assert response.status_code == 400, response.content

    # checking duplicate resource wasn't added
    response = user_client.list_resources()
    assert response.status_code == 200, response.content
    assert len(response.json()) == 1, response.json()

    # deleting
    response = user_client.delete_resource(resource_id)
    assert response.status_code == 200, response.content

    # getting resources
    response = user_client.list_resources()
    assert response.status_code == 200, response.content
    assert len(response.json()) == 0, response.json()


def test_forbidden_management_resorces_flow(db, client_factory):
    # init user1
    USER1_EMAIL = "user1@gmail.com"
    db.create_user(email=USER1_EMAIL, password=USER_PASSWORD)
    user1_client = client_factory.create_client()
    user1_client.authenticate(email=USER1_EMAIL, password=SUPERUSER_PASSWORD)

    # init user2
    USER2_EMAIL = "user2@gmail.com"
    user2_id = db.create_user(email=USER2_EMAIL, password=USER_PASSWORD)
    user2_client = client_factory.create_client()
    user2_client.authenticate(email=USER2_EMAIL, password=SUPERUSER_PASSWORD)

    # user2 create personal resource
    response = user2_client.create_resource(USER_RESOURCE_NAME)
    assert response.status_code == 201, response.content
    resource_id = response.json()["id"]

    # user1 try to get list resources other user
    response = user1_client.list_resources(user_id=user2_id)
    assert response.status_code == 403, response.content

    # user1 try to create resource other user
    response = user1_client.create_resource(
        user_id=user2_id, resource_name=USER_RESOURCE_NAME
    )
    assert response.status_code == 403, response.content

    # user1 try to delete resource other user
    response = user1_client.delete_resource(user_id=user2_id, resource_id=resource_id)
    assert response.status_code == 403, response.content


def test_management_user(superuser_client):
    superuser_client.authenticate(email=SUPERUSER_EMAIL, password=SUPERUSER_PASSWORD)

    # check exist only current user
    response = superuser_client.list_users()
    assert response.status_code == 200, response.content
    assert len(response.json()) == 1, response.json()

    # creating user
    response = superuser_client.create_user(email=USER_EMAIL, password=USER_PASSWORD)
    assert response.status_code == 201, response.content
    user_id = response.json()["id"]

    # check user was created
    response = superuser_client.list_users()
    assert response.status_code == 200, response.content
    assert len(response.json()) == 2, response.json()

    # attemt to create duplicate user
    response = superuser_client.create_user(email=USER_EMAIL, password=USER_PASSWORD)
    assert response.status_code == 400, response.content

    # check user wasn't added
    response = superuser_client.list_users()
    assert response.status_code == 200, response.content
    assert len(response.json()) == 2, response.json()

    # deleting user
    response = superuser_client.delete_user(user_id=user_id)
    assert response.status_code == 200, response.content

    # check exist only current user
    response = superuser_client.list_users()
    assert response.status_code == 200, response.content
    assert len(response.json()) == 1, response.json()


def test_management_user_resources(superuser_client):
    superuser_client.authenticate(email=SUPERUSER_EMAIL, password=SUPERUSER_PASSWORD)

    # creating user
    response = superuser_client.create_user(email=USER_EMAIL, password=USER_PASSWORD)
    assert response.status_code == 201, response.content
    user_id = response.json()["id"]

    # getting user resources
    response = superuser_client.list_resources(user_id=user_id)
    assert response.status_code == 200, response.content
    assert len(response.json()) == 0, response.json()

    # creating user resource
    response = superuser_client.create_resource(
        user_id=user_id, resource_name=USER_RESOURCE_NAME
    )
    assert response.status_code == 201, response.content
    resource_id = response.json()["id"]

    # getting user resources
    response = superuser_client.list_resources(user_id=user_id)
    assert response.status_code == 200, response.content
    assert len(response.json()) == 1, response.json()

    # deleting user
    response = superuser_client.delete_resource(
        user_id=user_id, resource_id=resource_id
    )
    assert response.status_code == 200, response.content

    # getting user resources
    response = superuser_client.list_resources(user_id=user_id)
    assert response.status_code == 200, response.content
    assert len(response.json()) == 0, response.json()


def test_quota_flow(superuser_client, client_factory):
    USER_RESOURCE1_NAME = "test user resource1"
    USER_RESOURCE2_NAME = "test user resource2"
    USER_RESOURCE3_NAME = "test user resource3"

    superuser_client.authenticate(email=SUPERUSER_EMAIL, password=SUPERUSER_PASSWORD)

    # creating user
    response = superuser_client.create_user(email=USER_EMAIL, password=USER_PASSWORD)
    assert response.status_code == 201, response.content
    user_id = response.json()["id"]

    # init user
    user_client = client_factory.create_client()
    user_client.authenticate(email=USER_EMAIL, password=USER_PASSWORD)

    # creating resource
    response = user_client.create_resource(USER_RESOURCE1_NAME)
    assert response.status_code == 201, response.content

    # superuser_client try to set not correct quota
    response = superuser_client.set_quota(user_id=user_id, quota=0)
    assert response.status_code == 406, response.content

    # superuser_client set correct quota
    response = superuser_client.set_quota(user_id=user_id, quota=2)
    assert response.status_code == 200, response.content

    # creating resource
    response = user_client.create_resource(USER_RESOURCE2_NAME)
    assert response.status_code == 201, response.content

    # getting resource
    response = user_client.list_resources()
    assert response.status_code == 200, response.content
    assert len(response.json()) == 2, response.json()

    # user try to create extra resource
    response = user_client.create_resource(USER_RESOURCE3_NAME)
    assert response.status_code == 406, response.content

    # getting resource
    response = user_client.list_resources()
    assert response.status_code == 200, response.content
    assert len(response.json()) == 2, response.json()
