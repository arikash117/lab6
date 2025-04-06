from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

test_user = [
    {
        'id': 3,
        'name': 'Test Testov',
        'email': 't.t.testov@mail.com',
    },
    {
        'id': 4,
        'name': 'BrrBrr Patapim',
        'email': 't.t.testov@mail.com'
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'test.test@mail.com'})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    response = client.post("/api/v1/user", json=test_user[0])
    assert response.status_code == 201
    assert response.json() == 3

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    response = client.post("/api/v1/user", json=test_user[1])
    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists"}

def test_delete_user():
    '''Удаление пользователя'''
    response = client.delete("/api/v1/user", params={'email': test_user[0]['email']})
    assert response.status_code == 204
    get_response = client.get("/api/v1/user", params={'email': test_user[0]['email']})
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "User not found"}
