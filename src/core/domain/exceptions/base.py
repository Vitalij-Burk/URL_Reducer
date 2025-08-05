from src.core.domain.logger import app_logger


class AppError(Exception):
    def __init__(self, module: str, *args, **kwargs):
        self.module = module


class NotFound(AppError):
    def __init__(self, module: str, resource, id):
        self.resource = resource
        self.id = id
        super().__init__(module, f"'{str(resource)}' '{str(id)}' not found.")


class Forbidden(AppError):
    def __init__(self, module: str, resource, current_id, req_id):
        self.resource = resource
        self.current_id = current_id
        self.req_id = req_id
        super().__init__(
            module,
            f"'{str(resource)} '{str(current_id)}' does not have access to '{req_id}'.",
        )


class LimitExceeded(AppError):
    def __init__(self, module: str, resource, exceeded):
        self.resource = resource
        self.exceeded = exceeded
        super().__init__(
            module, f"'{str(resource)}' limit of '{str(exceeded)}' exceeded."
        )


class Unauthorized(AppError):
    def __init__(self, module: str, resource, id):
        self.resource = resource
        self.id = id
        super().__init__(module, f"'{str(resource)}' '{str(id)}' unauthorized.")


class AlreadyExists(AppError):
    def __init__(self, module: str, resource, id):
        self.resource = resource
        self.id = id
        super().__init__(
            module, f"'{str(resource)}' with data '{str(id)}' already exists."
        )
