from helpers.generator import Generator

class InsufficientRegData:
    insufficient_reg_data = [
        {
            'email': Generator.email(),
            'password': Generator.password(),
            'name': ''
        },
        {
            'email': Generator.email(),
            'password': '',
            'name': Generator.name()
        },
        {
            'email': '',
            'password': Generator.password(),
            'name': Generator.name()
        }
    ]

class ResponseBodyError:
    # Регистрация пользователя
    CREATE_USER_ALREADY_EXIST = {'success': False,
                                 'message': 'User already exists'} #403 Forbidden
    CREATE_USER_NOT_ENOUGH_DATA = {'success': False,
                                   'message': 'Email, password and name are required fields'} #403 Forbidden
    # Авторизация пользователя
    LOGIN_USER_INCORRECT_DATA = {'success': False,
                                 'message': 'email or password are incorrect'} #401 Unauthorized
    # Создание заказа
    CREATE_ORDER_NOT_PASSED_INGREDIENTS = {'success': False,
                                           'message': 'Ingredient ids must be provided'} #400 Bad Request
    CREATE_ORDER_USER_UNAUTHORIZED = {'success': False,
                                      'message': 'You should be authorised'} #401 Unauthorized