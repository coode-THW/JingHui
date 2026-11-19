from typing import Any


class ApiError(Exception):
    def __init__(self, status_code: int, code: int, message: str, data: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
        self.data = data


def ok(data: Any = None, message: str = "success") -> dict[str, Any]:
    return {"code": 0, "message": message, "data": data}


def not_found(resource: str = "资源") -> ApiError:
    return ApiError(404, 40400, f"{resource}不存在")
