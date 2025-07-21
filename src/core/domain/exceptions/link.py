from src.core.domain.exceptions.base import AlreadyExists
from src.core.domain.exceptions.base import Forbidden
from src.core.domain.exceptions.base import LimitExceeded
from src.core.domain.exceptions.base import NotFound
from src.core.domain.exceptions.base import Unauthorized


class LinkNotFound(NotFound):
    def __init__(self, id):
        super().__init__("Link", id)


class LinkForbidden(Forbidden):
    def __init__(self, current_id, req_id):
        super().__init__("Link", current_id, req_id)


class LinkLimitExceeded(LimitExceeded):
    def __init__(self, exceeded):
        super().__init__("Link", exceeded)


class LinkUnauthorized(Unauthorized):
    def __init__(self, id):
        super().__init__("Link", id)


class LinkAlreadyExists(AlreadyExists):
    def __init__(self, id):
        super().__init__("Link", id)
