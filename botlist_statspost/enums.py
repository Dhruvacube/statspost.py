import enum

@enum.unique
class RequestTypes(enum.IntEnum):
    """Different requests types for the http request"""

    DELETE = 0
    GET = 1
    HEAD = 2
    PATCH = 3
    PUT = 4
    POST = 5
