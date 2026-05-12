from rest_framework.response import Response
from rest_framework import status as http_status
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.exceptions import ValidationError, PermissionDenied, NotAuthenticated, NotFound


AUTH_INVALID_CREDENTIALS = "AUTH_001"
AUTH_NOT_ADMIN = "AUTH_002"
AUTH_NOT_AUTHENTICATED = "AUTH_003"
AUTH_PERMISSION_DENIED = "AUTH_004"

USER_CANNOT_CHANGE_OWN_ROLE = "USER_001"
USER_CANNOT_DELETE_SELF = "USER_002"

EVENT_ONLY_DRAFT_PUBLISH = "EVENT_001"
EVENT_ONLY_DRAFT_DELETE = "EVENT_002"
EVENT_CLOSED_CANNOT_EDIT = "EVENT_003"
EVENT_ALREADY_CLOSED = "EVENT_004"
EVENT_CANNOT_CLOSE = "EVENT_005"
EVENT_NOT_FOUND = "EVENT_006"
EVENT_NO_AVAILABLE_SLOTS = "EVENT_007"

APPLICATION_NOT_ACCEPTING = "APP_001"
APPLICATION_EVENT_FULL = "APP_002"
APPLICATION_DUPLICATE = "APP_003"
APPLICATION_ONLY_PENDING = "APP_004"
APPLICATION_CANNOT_CHANGE = "APP_005"
APPLICATION_CANCELLED = "APP_006"
APPLICATION_NO_SLOTS = "APP_007"

FILE_IN_USE = "FILE_001"

VALIDATION_PASSWORD_MISMATCH = "VAL_001"
VALIDATION_OLD_PASSWORD_WRONG = "VAL_002"
VALIDATION_CODE_INVALID = "VAL_003"
VALIDATION_CODE_EXPIRED = "VAL_004"
VALIDATION_ALREADY_EXISTS = "VAL_005"
VALIDATION_UNSUPPORTED_FILTER = "VAL_006"
VALIDATION_BOOLEAN_PARAM = "VAL_007"
VALIDATION_FORM_INVALID = "VAL_008"

ERROR_MESSAGES = {
    AUTH_INVALID_CREDENTIALS: "Invalid student_id or password",
    AUTH_NOT_ADMIN: "Insufficient permissions: admin role required",
    AUTH_NOT_AUTHENTICATED: "Authentication credentials were not provided",
    AUTH_PERMISSION_DENIED: "You do not have permission to perform this action",
    USER_CANNOT_CHANGE_OWN_ROLE: "Cannot change your own role",
    USER_CANNOT_DELETE_SELF: "Cannot delete your own account",
    EVENT_ONLY_DRAFT_PUBLISH: "Only draft events can be published",
    EVENT_ONLY_DRAFT_DELETE: "Only draft events can be deleted",
    EVENT_CLOSED_CANNOT_EDIT: "Closed events cannot be edited",
    EVENT_ALREADY_CLOSED: "Event is already closed",
    EVENT_CANNOT_CLOSE: "Only published events that have not started can be closed",
    EVENT_NOT_FOUND: "Event not found",
    EVENT_NO_AVAILABLE_SLOTS: "This event has no available slots",
    APPLICATION_NOT_ACCEPTING: "This event is not accepting applications",
    APPLICATION_EVENT_FULL: "This event is already full",
    APPLICATION_DUPLICATE: "You have already applied to this event",
    APPLICATION_ONLY_PENDING: "Only pending applications can perform this action",
    APPLICATION_CANNOT_CHANGE: "This application decision cannot be changed",
    APPLICATION_CANCELLED: "Cancelled applications cannot be modified",
    APPLICATION_NO_SLOTS: "This event has no available slots",
    FILE_IN_USE: "File is in use and cannot be deleted",
    VALIDATION_PASSWORD_MISMATCH: "Passwords do not match",
    VALIDATION_OLD_PASSWORD_WRONG: "Old password is incorrect",
    VALIDATION_CODE_INVALID: "Invalid or non-existent verification code",
    VALIDATION_CODE_EXPIRED: "Verification code has expired",
    VALIDATION_ALREADY_EXISTS: "This value is already registered",
    VALIDATION_UNSUPPORTED_FILTER: "Unsupported filter value",
    VALIDATION_BOOLEAN_PARAM: "Boolean query parameter must be true or false",
    VALIDATION_FORM_INVALID: "Invalid form data",
}


def error_response(error_code, status_code=http_status.HTTP_400_BAD_REQUEST, detail=None):
    return Response(
        {
            "detail": detail or ERROR_MESSAGES.get(error_code, ""),
            "error_code": error_code,
        },
        status=status_code,
    )


_EXCEPTION_TO_CODE = {
    NotAuthenticated: (AUTH_NOT_AUTHENTICATED, http_status.HTTP_401_UNAUTHORIZED),
    PermissionDenied: (AUTH_PERMISSION_DENIED, http_status.HTTP_403_FORBIDDEN),
}


def custom_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)

    if response is not None:
        exc_type = type(exc)

        if exc_type in _EXCEPTION_TO_CODE:
            code, _ = _EXCEPTION_TO_CODE[exc_type]
            if isinstance(response.data, dict):
                response.data["error_code"] = code
        elif isinstance(exc, ValidationError):
            response.data = _with_error_code(response.data, VALIDATION_FORM_INVALID)
        elif isinstance(exc, NotFound):
            if isinstance(response.data, dict):
                response.data["error_code"] = EVENT_NOT_FOUND

    return response


def _with_error_code(data, error_code):
    if isinstance(data, dict):
        data["error_code"] = error_code
    elif isinstance(data, list):
        data = {"detail": data, "error_code": error_code}
    return data

