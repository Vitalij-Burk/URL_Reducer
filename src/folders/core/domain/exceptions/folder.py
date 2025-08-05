from src.core.domain.exceptions.base import AlreadyExists
from src.core.domain.exceptions.base import Forbidden
from src.core.domain.exceptions.base import LimitExceeded
from src.core.domain.exceptions.base import NotFound
from src.core.domain.exceptions.base import Unauthorized


class FolderNotFound(NotFound):
    def __init__(self, id):
        super().__init__("folders", "Folder", id)


class FolderForbidden(Forbidden):
    def __init__(self, current_id, req_id):
        super().__init__("folders", "Folder", current_id, req_id)


class FolderLimitExceeded(LimitExceeded):
    def __init__(self, exceeded):
        super().__init__("folders", "Folder", exceeded)


class FolderUnauthorized(Unauthorized):
    def __init__(self, id):
        super().__init__("folders", "Folder", id)


class FolderAlreadyExists(AlreadyExists):
    def __init__(self, id):
        super().__init__("folders", "Folder", id)
