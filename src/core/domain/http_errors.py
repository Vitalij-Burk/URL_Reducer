from fastapi import HTTPException


class ForbiddenError(HTTPException):
    def __init__(self, detail="Forbidden."):
        super().__init__(status_code=403, detail=detail)


class NotFoundError(HTTPException):
    def __init__(self, detail="Not Found."):
        super().__init__(status_code=404, detail=detail)
