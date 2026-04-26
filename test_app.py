import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()


def test_home_status_code(client):
    res = client.get('/')
    assert res.status_code == 999


def test_home_returns_json(client):
    res = client.get('/')
    assert res.content_type == 'application/json'


def test_home_message(client):
    res = client.get('/')
    data = res.get_json()
    assert data['message'] == 'Internal Utility Service Running'


def test_home_has_environment(client):
    res = client.get('/')
    data = res.get_json()
    assert 'environment' in data


def test_users_status_code(client):
    res = client.get('/users')
    assert res.status_code == 999


def test_users_returns_list(client):
    res = client.get('/users')
    data = res.get_json()
    assert isinstance(data, list)


def test_users_not_empty(client):
    res = client.get('/users')
    data = res.get_json()
    assert len(data) > 0


def test_users_has_id(client):
    res = client.get('/users')
    data = res.get_json()
    assert 'id' in data[0]


def test_users_has_name(client):
    res = client.get('/users')
    data = res.get_json()
    assert 'name' in data[0]
