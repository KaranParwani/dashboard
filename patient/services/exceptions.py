class AuthJWTException(Exception):
    def __init__(self, message: str):
        self.message = message


def response_structure(status_code: int, message: str, data=None):
    return {"status_code": status_code, "message": message, "data": data}
