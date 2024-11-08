import pytest
from app import app
from utils import create_user, update_user, delete_user


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def added_user_id(client):
    response = create_user(client, 'test@gmail.com', 'test')
    id = response.get_json()['user_id']
    yield id
    delete_user(client, id)


# Тест для проверки главной страницы
def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200  # Проверка, что код ответа 200 (OK)
    assert b'Hello, Docker!' in response.data  # Проверка, что текст 'Welcome' присутствует на странице


# Тест для маршрута, возвращающего данные
def test_data_page(client):
    response = client.get('/data')
    assert response.status_code == 200
    assert b'This is some data!' in response.data  # Проверка наличия кэшированных данных


def test_create_user(client):
    response = create_user(client, 'test@gmail.com', 'test')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'User created successfully'
    delete_user(client, response.get_json()['user_id'])


def test_update_user(client, added_user_id):
    response = update_user(client, added_user_id, 'updated_test', 'updated_test@gmail.com')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'User updated successfully'


def test_delete_user(client):
    id = create_user(client, 'test@gmail.com', 'test').get_json()['user_id']
    response = delete_user(client, id)
    assert response.status_code == 200
    assert response.get_json()['message'] == 'User deleted successfully'


def test_update_user_failed(client, added_user_id):
    response = update_user(client, 5344325, 'updated_test', 'updated_test@gmail.com')
    assert response.status_code == 404
    assert response.get_json()['message'] == 'User not found'


def test_delete_user_failed(client):
    response = delete_user(client, 5344325)
    assert response.status_code == 404
    assert response.get_json()['message'] == 'User not found'


def test_check_user_cache(client, added_user_id):
    old_response_username = client.get(f'/users/{added_user_id}').get_json()['username']

    new_username = "updated_test"
    update_user(client, added_user_id, new_username)

    new_response_username = client.get(f'/users/{added_user_id}').get_json()['username']

    assert new_response_username == old_response_username

