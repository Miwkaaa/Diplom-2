class Url:
    MAIN_URL = 'https://stellarburgers.education-services.ru/api'
    # Регистрация POST
    CREATE_USER = f"{MAIN_URL}/auth/register"
    # Авторизация POST
    LOGIN_USER = f"{MAIN_URL}/auth/login"
    # Создание заказа POST
    CREATE_ORDER = f"{MAIN_URL}/orders"
    # Удаление пользователя DELETE
    DELETE_USER = f"{MAIN_URL}/auth/user"
    # Получение данных об ингредиентах
    GET_INGREDIENTS = f"{MAIN_URL}/ingredients"
    # Получение данных о пользователе
    GET_USER_INFO = f"{MAIN_URL}/auth/user"