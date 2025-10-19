import pytest
import allure
import requests

from helpers.data import ResponseBodyError, InsufficientRegData
from helpers.endpoints import Url
from helpers.generator import Generator


@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.title("Создание нового пользователя")
    def test_create_user_unique_data_success(self, user_data_for_creation):
        user_data, register_token = user_data_for_creation
        with allure.step("Создание нового пользователя с использованием валидных данных регистрации"):
            response = requests.post(Url.CREATE_USER, json=user_data)
        with allure.step("Проверка успешной регистрации: код ответа 200 и accessToken в теле"):
            assert (response.status_code == 200 and "accessToken" in response.json())
            register_token = response.json()["accessToken"]


    @allure.title("Попытка повторной регистрации существующего пользователя")
    def test_create_user_duplicate_exists_user_error(self, registered_user):
        user_data, _ = registered_user
        with allure.step("Повторная регистрация с уже использованными данными"):
            response = requests.post(Url.CREATE_USER, json=user_data)
        with allure.step("Проверка получения ошибки: код ответа 403 и 'message': 'User already exists'"):
            assert (response.status_code == 403
                    and response.json() == ResponseBodyError.CREATE_USER_ALREADY_EXIST)

    @allure.title("Попытка регистрации без указания обязательного поля")
    @pytest.mark.parametrize("invalid_data", InsufficientRegData.insufficient_reg_data)
    def test_create_user_insufficient_data_error(self, invalid_data):
        with allure.step("При регистрации не передается поле email, name или password"):
            response = requests.post(Url.CREATE_USER, json=invalid_data)
        with allure.step("Проверка получения ошибки: код ответа 403 и "
                             "'message': 'Email, password and name are required fields'"):
            assert (response.status_code == 403
                    and response.json() == ResponseBodyError.CREATE_USER_NOT_ENOUGH_DATA)