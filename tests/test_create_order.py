import allure
import requests

from helpers.endpoints import Url
from helpers.data import ResponseBodyError
from helpers.generator import Generator


@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и добавлением ингредиентов")
    def test_create_order_user_login_success(self, registered_user):
        _, token = registered_user
        ingredients_ids = Generator.random_ingredients()
        with allure.step("Добавление ингредиентов и создание заказа"):
            response = requests.post(Url.CREATE_ORDER,
                                     json={'ingredients': ingredients_ids},
                                     headers={'Authorization': f'Bearer {token}'})
        with allure.step("Проверка успешного создания заказа: код ответа 200 и 'success' в теле"):
            assert response.status_code == 200 and response.json()['success'] is True


    @allure.title("Попытка создания заказа без ингредиентов")
    def test_create_order_without_ingredients_error(self, registered_user):
        _, token = registered_user
        with allure.step("Создание заказа без ингредиентов"):
            response = requests.post(Url.CREATE_ORDER,
                                     json={'ingredients': []},
                                     headers={'Authorization': f'Bearer {token}'})
        with allure.step("Проверка получения ошибки: код ответа 400 "
                             "и 'message': 'Ingredient ids must be provided'"):
            assert (response.status_code == 400
                    and response.json() == ResponseBodyError.CREATE_ORDER_NOT_PASSED_INGREDIENTS)

    @allure.title("Попытка создания заказа без авторизации пользователя")
    def test_create_order_unauthorized_user_error(self):
        with allure.step("Добавление ингредиентов без авторизации"):
            ingredients_ids = Generator.random_ingredients()
            response = requests.post(Url.CREATE_ORDER, json={'ingredients': ingredients_ids})
        with allure.step("Проверка получения ошибки: код ответа 401 "
                             "и 'message': 'You should be authorised'"):
            assert (response.status_code == 401
                    and response.json() == ResponseBodyError.CREATE_ORDER_USER_UNAUTHORIZED)

    @allure.title("Попытка создания заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_hash_error(self, registered_user):
        _, token = registered_user
        invalid_ingredients_id = Generator.random_invalid_id()
        with allure.step("При создании заказа передается неверный хэш"):
            response = requests.post(Url.CREATE_ORDER,
                                     json={'ingredients': [invalid_ingredients_id]},
                                     headers={'Authorization': f'Bearer {token}'})
        with allure.step("Проверка получения ошибки: код ответа 500"):
            assert response.status_code == 500