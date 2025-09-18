from src.models import Error, ErrorType


def parse_error(json: dict) -> Error:
    return Error(
        error_type=ErrorType[json["errorType"]],
        message=json["message"],
    )