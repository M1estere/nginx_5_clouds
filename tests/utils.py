mock_email = "test_email@tst.tst"
mock_username = "test_username"


def create_user(client, email, username):
    """Create new user"""
    response = client.post(
        '/users',
        json={
            "username": username,
            "email": email,
        }
    )
    return response


def delete_user(client, user_id):
    """Delete user by id"""
    response = client.delete(f'/users/{user_id}')
    return response


def update_user(client, user_id, username, email=None):
    """Update user by id"""
    response = client.put(
        f'/users/{user_id}',
        json={
            "username": username,
            "email": email,
        }
    )
    return response


def validate_json(schema, response_json):
    """Validate response json with schema"""
    if isinstance(response_json, list):
        assert schema.model_validate(response_json[0])
    else:
        assert schema.model_validate(response_json)
