import allure
import requests

from helpers.endpoints import Url
from helpers.data import ResponseBodyError


@allure.feature("Авторизация пользователя")
class TestLoginUser:

    @allure.title("Вход под зарегистрированным пользователем")
    def test_login_user_existing_user_success(self, registered_user):
        user_data, token = registered_user
        with allure.step("Авторизация с данными, использованными при регистрации"):
            response = requests.post(Url.LOGIN_USER, json={
                'email': user_data['email'],
                'password': user_data['password']
            })
        with allure.step("Проверка успешной авторизации: код ответа 200 и accessToken в теле"):
            assert (response.status_code == 200 and "accessToken" in response.json())

    @allure.title("Попытка авторизации с неверным email")
    def test_login_user_wrong_email_error(self, registered_user):
        user_data, _ = registered_user
        with allure.step("Вход с указанием неверного email и верным паролем"):
            test_data = {'email': "invalidmail@google.com", 'password': user_data['password']}
            response = requests.post(Url.LOGIN_USER, json=test_data)
        with allure.step("Проверка появления ошибки: код ответа 400 "
                             "и 'message': 'email or password are incorrect'"):
            assert (response.status_code == 401
                    and response.json() == ResponseBodyError.LOGIN_USER_INCORRECT_DATA)

    @allure.title("Попытка авторизации с неверным паролем")
    def test_login_user_wrong_password_error(self, registered_user):
        user_data, _ = registered_user
        with allure.step("Вход с указанием верного email и неверного пароля"):
            test_data = {'email': user_data['email'], 'password': "invalidspass"}
            response = requests.post(Url.LOGIN_USER, json=test_data)
        with allure.step("Проверка появления ошибки: код ответа 400 "
                             "и 'message': 'email or password are incorrect'"):
            assert (response.status_code == 401
                    and response.json() == ResponseBodyError.LOGIN_USER_INCORRECT_DATA)

    @allure.title("Попытка авторизации с пустым email")
    def test_login_user_empty_email_error(self, registered_user):
        user_data, _ = registered_user
        with allure.step("Вход без email и верным паролем"):
            test_data = {'email': "", 'password': user_data['password']}
            response = requests.post(Url.LOGIN_USER, json=test_data)
        with allure.step("Проверка появления ошибки: код ответа 400 "
                             "и 'message': 'email or password are incorrect'"):
            assert (response.status_code == 401
                    and response.json() == ResponseBodyError.LOGIN_USER_INCORRECT_DATA)

    @allure.title("Попытка авторизации с пустым паролем")
    def test_login_user_empty_password_error(self, registered_user):
        user_data, _ = registered_user
        with allure.step("Вход с указанием верного email и пустым пвролем"):
            test_data = {'email': user_data['email'], 'password': ""}
            response = requests.post(Url.LOGIN_USER, json=test_data)
        with allure.step("Проверка появления ошибки: код ответа 400 "
                             "и 'message': 'email or password are incorrect'"):
            assert (response.status_code == 401
                    and response.json() == ResponseBodyError.LOGIN_USER_INCORRECT_DATA)