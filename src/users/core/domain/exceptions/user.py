from src.core.domain.exceptions.base import AlreadyExists
from src.core.domain.exceptions.base import Forbidden
from src.core.domain.exceptions.base import LimitExceeded
from src.core.domain.exceptions.base import NotFound
from src.core.domain.exceptions.base import Unauthorized


class UserNotFound(NotFound):
    def __init__(self, id):
        super().__init__("users", "User", id)


class UserForbidden(Forbidden):
    def __init__(self, current_id, req_id):
        super().__init__("users", "User", current_id, req_id)


class UserLimitExceeded(LimitExceeded):
    def __init__(self, exceeded):
        super().__init__("users", "User", exceeded)


class UserUnauthorized(Unauthorized):
    def __init__(self, id):
        super().__init__("users", "User", id)


class UserAlreadyExists(AlreadyExists):
    def __init__(self, id):
        super().__init__("users", "User", id)
