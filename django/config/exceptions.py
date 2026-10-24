from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return None

    if isinstance(exc, ValidationError):
        errors = response.data
        fields = errors if isinstance(errors, dict) else {}
        known_errors = (
            ("name", "Role name already exists."),
            ("code", "Code already exists."),
        )
        detail = next((message for field, message in known_errors
                       if any(str(error) == message for error in fields.get(field, []))),
                      "Invalid request.")
        response.data = {"detail": detail}
    elif response.status_code in (401, 403, 404):
        response.data = None

    return response
