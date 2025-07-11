from dataclasses import dataclass

from src.core.domain.schemas.inner.user import UserResponseInner
from src.core.domain.schemas.safe.user import UserResponse


@dataclass
class FakeUserCollection:
    safe: UserResponse
    inner: UserResponseInner
