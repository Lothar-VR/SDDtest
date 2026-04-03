"""
Error handlers and exception definitions
"""
from fastapi import HTTPException, status
from pydantic import ValidationError


class EmployeeNotFoundError(Exception):
    """Raised when employee is not found"""
    pass


class EmployeeEmailConflictError(Exception):
    """Raised when email already exists"""
    pass


def handle_employee_not_found(detail: str = "Employee not found") -> HTTPException:
    """
    Handle employee not found errors
    """
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail
    )


def handle_email_conflict(detail: str = "Email already exists") -> HTTPException:
    """
    Handle email conflict errors
    """
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=detail
    )


def handle_validation_error(detail: str = "Invalid input data") -> HTTPException:
    """
    Handle validation errors
    """
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=detail
    )


def handle_internal_error(detail: str = "Internal server error") -> HTTPException:
    """
    Handle internal server errors
    """
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=detail
    )


def format_error_response(status_code: int, detail: str, error_type: str = None) -> dict:
    """
    Format standard error response
    """
    return {
        "status_code": status_code,
        "detail": detail,
        "error_type": error_type or "Error"
    }
