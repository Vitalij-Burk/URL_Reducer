from uuid import uuid4

import pytest

from src.core.domain.schemas.inner.link import LinkResponseInner
from src.core.domain.schemas.inner.user import UserResponseInner
from src.core.domain.schemas.safe.link import LinkResponse
from src.core.domain.schemas.safe.user import UserResponse
from tests.app.services.unit.schemas.link import FakeLinkCollection
from tests.app.services.unit.schemas.user import FakeUserCollection


@pytest.fixture
def fake_users():
    user_id = uuid4()
    return FakeUserCollection(
        inner=UserResponseInner(
            user_id=user_id,
            email="test@mail.com",
            name="tester",
            hashed_password="fdasfasfd",
            links=[],
        ),
        safe=UserResponse(
            user_id=user_id, email="test@mail.com", name="tester", links=[]
        ),
    )


@pytest.fixture
def fake_links():
    link_id = uuid4()
    user_id = uuid4()
    return FakeLinkCollection(
        inner=LinkResponseInner(
            link_id=link_id,
            user_id=user_id,
            name="test",
            original_url="https://yt.com",
            short_code="f12Qsds3",
            clicks=1,
        ),
        safe=LinkResponse(
            link_id=link_id,
            user_id=user_id,
            name="test",
            original_url="https://yt.com",
            short_url="http://localhost:8000/f12Qsds3",
            short_code="f12Qsds3",
            clicks=1,
        ),
    )
