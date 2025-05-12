class UserAlreadyExistsError(Exception):
    pass


class IncorrectPasswordOrEmailError(Exception):
    pass


class JWTIsEmptyError(Exception):
    pass


class InvalidTokenError(Exception):
    pass


class JWTIsFiredError(Exception):
    pass
