class LoginNotFound(Exception):
    def __str__(self):
        return 'Пользователь не найден'

class PasswordError(Exception):
    def __str__(self):
        return 'Неверный пароль'

class KeyError(Exception):
    def __str__(self):
        return 'Неверный ключ активации продукта'