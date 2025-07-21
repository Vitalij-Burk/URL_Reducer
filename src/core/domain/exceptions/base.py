from src.core.domain.logger import logger


class AppError(Exception):
    pass


class NotFound(AppError):
    def __init__(self, resource, id):
        self.resource = resource
        self.id = id
        super().__init__(f"'{str(resource)}' '{str(id)}' not found.")


class Forbidden(AppError):
    def __init__(self, resource, current_id, req_id):
        self.resource = resource
        self.current_id = current_id
        self.req_id = req_id
        super().__init__(
            f"'{str(resource)} '{str(current_id)}' does not have access to '{req_id}'."
        )


class LimitExceeded(AppError):
    def __init__(self, resource, exceeded):
        self.resource = resource
        self.exceeded = exceeded
        super().__init__(f"'{str(resource)}' limit of '{str(exceeded)}' exceeded.")


class Unauthorized(AppError):
    def __init__(self, resource, id):
        self.resource = resource
        self.id = id
        super().__init__(f"'{str(resource)}' '{str(id)}' unauthorized.")


class AlreadyExists(AppError):
    def __init__(self, resource, id):
        self.resource = resource
        self.id = id
        super().__init__(f"'{str(resource)}' with data '{str(id)}' already exists.")
