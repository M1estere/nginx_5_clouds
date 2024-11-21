import pytest
from main import app
from .shemes import UsersResponse
from .utils import create_user, mock_email, mock_username, delete_user, validate_json, update_user


@pytest.fixture
def client():
    """Returns app client"""
    with app.test_client() as client:
        yield client


@pytest.fixture
def new_user_id(client):
    """Create user return user_id"""
    response = create_user(client, mock_email, mock_username)
    user_id = response.get_json()['user_id']
    yield user_id
    delete_user(client, user_id)


def test_home_page(client):
    """Test for home route"""
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_data(as_text=True) == """
    <h1>Вы че тут забыли а?? Я НЕНАВИЖУ ДЕВОПС!</h1>
    """


def test_get_users_response(client, new_user_id):
    """Test get all users"""
    response = client.get('/users')
    assert response.status_code == 200
    validate_json(UsersResponse, response.get_json())


def test_get_user_response(client, new_user_id):
    """Test get user by id"""
    response = client.get(f'/user/{new_user_id}')
    assert response.status_code == 200
    validate_json(UsersResponse, response.get_json())


def test_create_user_response(client):
    """Test create user"""
    try:
        response = create_user(client, mock_email, mock_username)
        assert response.status_code == 200
        assert response.get_json()['message'] == 'User created successfully'
    finally:
        delete_user(client, response.get_json()['user_id'])


def test_create_user_already_exists(client, new_user_id):
    """Test create user 404 error"""
    response = create_user(client, mock_email, mock_username)
    assert response.status_code == 404
    assert response.get_json()['message'] == 'User already exists'


def test_delete_user_response(client):
    """Test delete user by id"""
    user_id = create_user(client, mock_email, mock_username).get_json()['user_id']
    response = delete_user(client, user_id)
    assert response.status_code == 200
    assert response.get_json()['message'] == 'User deleted successfully'


def test_delete_user_not_founded(client):
    """Test delete user by id"""
    response = delete_user(client, 100010001000)
    assert response.status_code == 404
    assert response.get_json()['message'] == 'User not founded'


def test_update_user_response(client, new_user_id):
    """Test update user by id"""
    new_username = "changed_username"
    response = update_user(client, new_user_id, new_username)
    assert response.status_code == 200
    assert response.get_json()['message'] == 'User updated successfully'


def test_update_user_not_founded(client, new_user_id):
    """Test update user by id"""
    response = update_user(client, 100010001000, "smth")
    assert response.status_code == 404
    assert response.get_json()['message'] == 'User not founded'


def test_check_user_cache(client, new_user_id):
    """Test check chache on endpoint"""
    old_response_username = client.get(f'/user/{new_user_id}').get_json()['username']

    new_username = "new_username"
    update_user(client, new_user_id, new_username)

    new_response_username = client.get(f'/user/{new_user_id}').get_json()['username']

    assert new_response_username == old_response_username


def test_check_clear_cache(client, new_user_id):
    """Test clear cache check"""
    old_response_username = client.get(f'/user/{new_user_id}').get_json()['username']

    new_username = "new_username"
    update_user(client, new_user_id, new_username)

    new_response_username = client.get(f'/user/{new_user_id}').get_json()['username']
    assert new_response_username == old_response_username

    client.get(f'/clear_cache/{new_user_id}')

    new_response_username_2 = client.get(f'/user/{new_user_id}').get_json()['username']
    assert new_response_username_2 == new_username
