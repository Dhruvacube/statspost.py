class HttpException(Exception):
    """
    AsyncDagpi base exception class use this base class to catch any AsyncDagpi errors.
    """

    def __init__(self, status: int, message: str) -> None:
        self.status: int = status
        self.message: str = message
        super().__init__(message)


class ApiError(HttpException):
    """
    Raised when Fluxpoint has an error it does not know how to handle
    """

    def __init__(self, message: str) -> None:
        super().__init__(500, message)


class WrongReturnType(Exception):
    """
    Exception raised when the when wrong return type is given
    """


class Unauthorised(HttpException):
    """
    Raised for an API 401
    """

    def __init__(self, message: str) -> None:
        super().__init__(401, message)


class RateLimited(HttpException):
    """
    You are exceeding the API's rate limits and built in Ratelimit handler
    Essentially a 429
    """

    def __init__(self, message: str) -> None:
        super().__init__(429, message)


class ParameterError(HttpException):
    """
    Parameters passed were not Sufficient
    """

    def __init__(self, message: str) -> None:
        super().__init__(400, message)
