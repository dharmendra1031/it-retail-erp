from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return None

    if isinstance(exc, ValidationError):
        errors = response.data
        values = errors.values() if isinstance(errors, dict) else errors if isinstance(errors, list) else [errors]
        messages = [str(error) for value in values
                    for error in (value if isinstance(value, list) else [value])]
        known_errors = (
            "Role name already exists.",
            "Code already exists.",
            "Category code already exists.",
            "Brand code already exists.",
            "Unit code already exists.",
            "SKU or barcode already exists.",
        )
        detail = next((message for message in known_errors if message in messages), "Invalid request.")
        response.data = {"detail": detail}
    elif response.status_code in (401, 403, 404):
        response.data = None

    return response
