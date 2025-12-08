import json

def test_register(client, init_db):
    # Test user registration
    username, email, password = 'testuser', 'testuser@example.com', 'testPassword@1'
    response = client.post('/api/auth/register', json={
        'username': username,
        'email': email,
        'password': password
    })
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 201
    assert result['message'] == 'User created successfully'
    assert result['data']['username'] == username
    assert result['data']['email'] == email
    assert result['data']['role']['name'] == 'user'
    assert result['data']['created_at'] is not None
    assert result['data']['updated_at'] is not None


def test_login(client, init_db):
    # Test user login
    username, email, password = 'user', 'user@example.com', 'user'
    response = client.post('/api/auth/login', json={
        'email': email,
        'password': password
    })
    result = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert result['message'] == 'Login successful'
    assert 'access_token' in result['data']
    assert 'data' in result
    assert result['data']['user']['username'] == username
    assert result['data']['user']['email'] == email
    assert result['data']['user']['role']['name'] == 'user'
    assert result['data']['user']['created_at'] is not None
    assert result['data']['user']['updated_at'] is not None
