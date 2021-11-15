from enum import Enum


class expected_result(Enum):
    as_expected = 1
    not_expected = 0


"""
200 OK
201 Created
204 No Content => deleted
400 Bad Request
"""


class http_result(Enum):
    OK = 200
    Created = 201
    NoContentDeleted = 204
    BadRequest = 400
