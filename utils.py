from app import app


# добавление пользователя
def create_user(client, email, username):
    response = client.post(
        '/users',
        json={
            "username": username,
            "email": email,
        }
    )
    return response


# удаление пользователя
def delete_user(client, id):
    response = client.delete(f'/users/{id}')
    return response


# обновление пользователя
def update_user(client, id, username, email='default@gmail.com'):
    response = client.put(
        f'/users/{id}',
        json={
            "username": username,
            "email": email,
        }
    )
    return response