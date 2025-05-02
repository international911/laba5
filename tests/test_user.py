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

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'nonexistent@mail.com'})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user = {
        'name': 'NEW USER',
        'email': 'new.user@mail.com'
    }
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    assert isinstance(response.json(), int)

    # Проверка на создание пользователя
    check_response = client.get("/api/v1/user", params={'email': new_user['email']})
    assert check_response.status_code == 200
    assert check_response.json()['email'] == new_user['email']

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    existing_user = {
        'name': 'DUPLICATE USER',
        'email': users[0]['email']
    }
    response = client.post("/api/v1/user", json=existing_user)
    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists"}

def test_delete_user():
    '''Удаление пользователя'''
    # Создание пользователя для теста удаления
    temp_user = {
        'name': 'TEST USER',
        'email': 'test.user@mail.com'
    }
    create_response = client.post("/api/v1/user", json=temp_user)
    user_id = create_response.json()

    # Удаление пользователя
    delete_response = client.delete("/api/v1/user", params={'email': temp_user['email']})
    assert delete_response.status_code == 204

    # Проверка на удаление пользователя
    check_response = client.get("/api/v1/user", params={'email': temp_user['email']})
    assert check_response.status_code == 404
