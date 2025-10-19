import pytest
import requests

from helpers.generator import Generator
from helpers.endpoints import Url


@pytest.fixture
# Зарегистрированный и авторизованный пользователь
def registered_user():
    user_data = Generator.user_data()
    # Регистрация пользователя
    registration_response = requests.post(Url.CREATE_USER, json=user_data)
    assert registration_response.status_code == 200, \
        f"Не удалось зарегистрироваться: {registration_response.text}"
    # Авторизация пользователя
    login_response = requests.post(Url.LOGIN_USER, json={
        "email": user_data["email"],
        "password": user_data["password"]
    })
    assert login_response.status_code == 200, \
        f"Не удалось войти: {login_response.text}"
    # Получение accessToken
    token = login_response.json().get("accessToken", "")
    if token.startswith("Bearer "):
        token = token.split(" ", 1)[1]
    yield user_data, token
    # Удаление пользователя
    requests.delete(Url.DELETE_USER, headers={"Authorization": f"Bearer {token}"})

@pytest.fixture
# Генерация данных для создания пользователя и удаление его по accessToken
def user_data_for_creation():
    user_data = Generator.user_data()
    token = None
    yield user_data, lambda t: globals().update(token := t)
    if token:
        requests.delete(Url.DELETE_USER, headers={"Authorization": f"Bearer {token}"})