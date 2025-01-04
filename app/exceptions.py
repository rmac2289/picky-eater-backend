from http import HTTPStatus
from fastapi import HTTPException


class UserIdMismatchException(HTTPException):
    def __init__(self, detail: str = "ID in request does not match current user."):
        super().__init__(status_code=HTTPStatus.FORBIDDEN, detail=detail)

class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Resource not found."):
        super().__init__(status_code=HTTPStatus.NOT_FOUND)