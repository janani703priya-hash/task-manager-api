import pytest
from app import app, db
from flask import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200

def test_register(client):
    response = client.post('/register', 
        json={'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 201

def test_login(client):
    client.post('/register',
        json={'username': 'testuser', 'password': 'testpass'})
    response = client.post('/login',
        json={'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 200
    assert 'token' in response.get_json()