from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return None

    if isinstance(exc, ValidationError):
        errors = response.data
        name_errors = errors.get("name", []) if isinstance(errors, dict) else []
        if any(str(message) == "Role name already exists." for message in name_errors):
            response.data = {"detail": "Role name already exists."}
        else:
            response.data = {"detail": "Invalid request."}
    elif response.status_code in (401, 403, 404):
        response.data = None

    return response
