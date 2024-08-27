import pytest
from flask import Flask
from app import create_app, db
from app.models import QueryHistory

@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_root(client):
    response = client.get('/')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['version'] == "0.1.0"
    assert 'date' in json_data
    assert 'kubernetes' in json_data

def test_lookup_valid_domain(client):
    response = client.post('/v1/tools/lookup', json={"domain": "example.com"})
    assert response.status_code == 200
    json_data = response.get_json()
    assert isinstance(json_data, list)
    assert len(json_data) > 0

def test_lookup_invalid_domain(client):
    response = client.post('/v1/tools/lookup', json={"domain": "invalid.domain"})
    assert response.status_code == 500
    json_data = response.get_json()
    assert "error" in json_data

def test_validate_valid_ip(client):
    response = client.post('/v1/tools/validate', json={"address": "8.8.8.8"})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['valid'] is True

def test_validate_invalid_ip(client):
    response = client.post('/v1/tools/validate', json={"address": "999.999.999.999"})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['valid'] is False