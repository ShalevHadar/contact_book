from typing import Any, Callable
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from sqlalchemy.exc import SQLAlchemyError


class ContactException(Exception):
    pass


class ContactNotFound(ContactException):
    pass


class ContactAlreadyExists(ContactException):
    pass


class InvalidPageNumber(Exception):
    pass


class InvalidPhoneNumber(Exception):
    pass


class InvalidSearch(Exception):
    pass


def create_exception_handler(
    status_code: int, initial_detail: Any
) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: ContactException):
        return JSONResponse(content=initial_detail, status_code=status_code)

    return exception_handler


def register_all_errors(app: FastAPI):
    app.add_exception_handler(
        InvalidSearch,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Invalid Search Parameters",
                "error_code": "400",
            },
        ),
    )

    app.add_exception_handler(
        ContactAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "A contact with this phone number already exists.",
                "error_code": "400",
            },
        ),
    )

    app.add_exception_handler(
        ContactNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Contact not found",
                "error_code": "404",
            },
        ),
    )

    app.add_exception_handler(
        InvalidPageNumber,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Invalid Page Number",
                "error_code": "400",
            },
        ),
    )

    app.add_exception_handler(
        InvalidPhoneNumber,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Invalid Phone Number",
                "error_code": "400",
            },
        ),
    )

    @app.exception_handler(SQLAlchemyError)
    async def database__error(request, exc):
        print(str(exc))
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": "500",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
