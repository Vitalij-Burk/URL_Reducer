import json
import random
from dataclasses import asdict
from uuid import uuid4

import pytest
from pydantic import EmailStr
from pydantic import HttpUrl
from pydantic import TypeAdapter

from src.core.domain.schemas.dataclasses.link import CreateLinkInner
from src.core.domain.schemas.dataclasses.link import DeletedLinkResponseInner
from src.core.domain.schemas.dataclasses.link import LinkResponseInner
from src.core.domain.schemas.dataclasses.link import UpdateLinkRequestInner
from src.core.domain.schemas.dataclasses.user import CreateUserInner
from src.core.domain.schemas.dataclasses.user import DeletedUserResponseInner
from src.core.domain.schemas.dataclasses.user import UpdateUserRequestInner
from src.core.domain.schemas.dataclasses.user import UserResponseInner
from src.core.domain.schemas.pydantic.link import CreateLink
from src.core.domain.schemas.pydantic.link import DeletedLinkResponse
from src.core.domain.schemas.pydantic.link import LinkResponse
from src.core.domain.schemas.pydantic.link import UpdateLinkRequest
from src.core.domain.schemas.pydantic.user import CreateUser
from src.core.domain.schemas.pydantic.user import DeletedUserResponse
from src.core.domain.schemas.pydantic.user import UpdateUserRequest
from src.core.domain.schemas.pydantic.user import UserResponse
from src.core.utils.serializers.cache.to.link import _deep_encoder as _deep_link_encoder
from src.core.utils.serializers.cache.to.user import _deep_encoder as _deep_user_encoder
from tests.schemas.link import FakeLinkCollection
from tests.schemas.user import FakeUserCollection


user_id = uuid4()


@pytest.fixture
def fake_users():
    name = "tester"
    email = "tester@mail.com"
    password = "string"
    hashed_password = "hashed_string"
    links = []
    return FakeUserCollection(
        cache=json.dumps(
            asdict(
                UserResponseInner(
                    user_id=user_id,
                    name=name,
                    email=email,
                    hashed_password=hashed_password,
                    links=links,
                )
            ),
            default=_deep_user_encoder,
        ),
        safe_resp=UserResponse(
            user_id=user_id,
            name=name,
            email=TypeAdapter(EmailStr).validate_python(email),
            links=links,
        ),
        inner_resp=UserResponseInner(
            user_id=user_id,
            name=name,
            email=email,
            hashed_password=hashed_password,
            links=links,
        ),
        safe_del=DeletedUserResponse(deleted_user_id=user_id),
        inner_del=DeletedUserResponseInner(deleted_user_id=user_id),
        safe_create=CreateUser(
            name=name,
            email=TypeAdapter(EmailStr).validate_python(email),
            password=password,
        ),
        inner_create=CreateUserInner(
            name=name, email=email, hashed_password=hashed_password
        ),
        safe_update=UpdateUserRequest(
            email=TypeAdapter(EmailStr).validate_python(email), name=name
        ),
        inner_update=UpdateUserRequestInner(email=email, name=name),
    )


@pytest.fixture
def fake_links():
    link_id = uuid4()
    name = "test"
    original_url = "https://youtube.com/"
    short_code = "fadfaS12"
    short_url = "http://localhost:8000/fadfaS12"
    clicks = random.randint(0, 9)
    return FakeLinkCollection(
        cache=json.dumps(
            asdict(
                LinkResponseInner(
                    link_id=link_id,
                    user_id=user_id,
                    name=name,
                    original_url=original_url,
                    short_code=short_code,
                    clicks=clicks,
                )
            ),
            default=_deep_link_encoder,
        ),
        safe_resp=LinkResponse(
            link_id=link_id,
            user_id=user_id,
            name=name,
            original_url=HttpUrl(original_url),
            short_url=HttpUrl(short_url),
            short_code=short_code,
            clicks=clicks,
        ),
        inner_resp=LinkResponseInner(
            link_id=link_id,
            user_id=user_id,
            name=name,
            original_url=original_url,
            short_code=short_code,
            clicks=clicks,
        ),
        safe_del=DeletedLinkResponse(deleted_link_id=link_id),
        inner_del=DeletedLinkResponseInner(deleted_link_id=link_id),
        safe_create=CreateLink(name=name, original_url=HttpUrl(original_url)),
        inner_create=CreateLinkInner(
            user_id=user_id, name=name, original_url=original_url, short_code=short_code
        ),
        safe_update=UpdateLinkRequest(name=name),
        inner_update=UpdateLinkRequestInner(name=name),
    )
