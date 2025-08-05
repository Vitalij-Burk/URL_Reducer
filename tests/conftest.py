import json
import random
from dataclasses import asdict
from uuid import uuid4

import pytest
from pydantic import EmailStr
from pydantic import HttpUrl
from pydantic import TypeAdapter

from src.folders.core.domain.schemas.inner.folder import CreateFolderRequestInner
from src.folders.core.domain.schemas.inner.folder import DeletedFolderResponseInner
from src.folders.core.domain.schemas.inner.folder import FolderResponseInner
from src.folders.core.domain.schemas.inner.folder import MoveFolderRequestInner
from src.folders.core.domain.schemas.inner.folder import UpdateFolderRequestInner
from src.folders.core.domain.schemas.out.folder import CreateFolderRequest
from src.folders.core.domain.schemas.out.folder import DeletedFolderResponse
from src.folders.core.domain.schemas.out.folder import FolderResponse
from src.folders.core.domain.schemas.out.folder import MoveFolderRequest
from src.folders.core.domain.schemas.out.folder import UpdateFolderRequest
from src.folders.core.utils.serializers.folder.cache.to import (
    _deep_encoder as deep_folder_encoder,
)
from src.folders.infrastructure.storages.db.base.models import Folder
from src.links.core.domain.schemas.inner.link import CreateLinkRequestInner
from src.links.core.domain.schemas.inner.link import DeletedLinkResponseInner
from src.links.core.domain.schemas.inner.link import LinkResponseInner
from src.links.core.domain.schemas.inner.link import MoveLinkRequestInner
from src.links.core.domain.schemas.inner.link import UpdateLinkRequestInner
from src.links.core.domain.schemas.out.link import CreateLinkRequest
from src.links.core.domain.schemas.out.link import DeletedLinkResponse
from src.links.core.domain.schemas.out.link import LinkResponse
from src.links.core.domain.schemas.out.link import MoveLinkRequest
from src.links.core.domain.schemas.out.link import UpdateLinkRequest
from src.links.core.utils.serializers.link.cache.to import (
    _deep_encoder as deep_link_encoder,
)
from src.links.infrastructure.storages.db.base.models import Link
from src.users.core.domain.schemas.inner.user import CreateUserRequestInner
from src.users.core.domain.schemas.inner.user import DeletedUserResponseInner
from src.users.core.domain.schemas.inner.user import UpdateUserRequestInner
from src.users.core.domain.schemas.inner.user import UserResponseInner
from src.users.core.domain.schemas.out.user import CreateUserRequest
from src.users.core.domain.schemas.out.user import DeletedUserResponse
from src.users.core.domain.schemas.out.user import UpdateUserRequest
from src.users.core.domain.schemas.out.user import UserResponse
from src.users.core.utils.serializers.cache.to import _deep_encoder as deep_user_encoder
from src.users.infrastructure.storages.db.base.models import User
from tests.schemas.folder import FakeFolderCollection
from tests.schemas.link import FakeLinkCollection
from tests.schemas.user import FakeUserCollection


user_id = uuid4()
link_id = uuid4()
folder_id = uuid4()


@pytest.fixture
def fake_users():
    name = "tester"
    email = "tester@mail.com"
    password = "string!1234"
    hashed_password = "hashed_string"
    link_ids = []
    folder_ids = []
    return FakeUserCollection(
        cache=json.dumps(
            asdict(
                UserResponseInner(
                    user_id=user_id,
                    name=name,
                    email=email,
                    hashed_password=hashed_password,
                    link_ids=link_ids,
                    folder_ids=folder_ids,
                )
            ),
            default=deep_user_encoder,
        ),
        safe_resp=UserResponse(
            user_id=user_id,
            name=name,
            email=TypeAdapter(EmailStr).validate_python(email),
            link_ids=link_ids,
            folder_ids=folder_ids,
        ),
        inner_resp=UserResponseInner(
            user_id=user_id,
            name=name,
            email=email,
            hashed_password=hashed_password,
            link_ids=link_ids,
            folder_ids=folder_ids,
        ),
        safe_del=DeletedUserResponse(deleted_user_id=user_id),
        inner_del=DeletedUserResponseInner(deleted_user_id=user_id),
        safe_create=CreateUserRequest(
            name=name,
            email=TypeAdapter(EmailStr).validate_python(email),
            password=password,
        ),
        inner_create=CreateUserRequestInner(
            name=name, email=email, hashed_password=hashed_password
        ),
        safe_update=UpdateUserRequest(
            email=TypeAdapter(EmailStr).validate_python(email), name=name
        ),
        inner_update=UpdateUserRequestInner(email=email, name=name),
    )


@pytest.fixture
def fake_links():
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
                    folder_id=folder_id,
                )
            ),
            default=deep_link_encoder,
        ),
        safe_resp=LinkResponse(
            link_id=link_id,
            user_id=user_id,
            name=name,
            original_url=HttpUrl(original_url),
            short_url=HttpUrl(short_url),
            short_code=short_code,
            clicks=clicks,
            folder_id=folder_id,
        ),
        inner_resp=LinkResponseInner(
            link_id=link_id,
            user_id=user_id,
            name=name,
            original_url=original_url,
            short_code=short_code,
            clicks=clicks,
            folder_id=folder_id,
        ),
        safe_del=DeletedLinkResponse(deleted_link_id=link_id),
        inner_del=DeletedLinkResponseInner(deleted_link_id=link_id),
        safe_create=CreateLinkRequest(
            name=name, original_url=HttpUrl(original_url), folder_id=folder_id
        ),
        inner_create=CreateLinkRequestInner(
            user_id=user_id,
            name=name,
            original_url=original_url,
            short_code=short_code,
            folder_id=folder_id,
        ),
        safe_update=UpdateLinkRequest(name=name),
        inner_update=UpdateLinkRequestInner(name=name),
        safe_move=MoveLinkRequest(folder_id=None),
        inner_move=MoveLinkRequestInner(folder_id=None),
    )


@pytest.fixture
def fake_folders():
    parent_id = None
    name = "string"
    choldren_ids = []
    link_ids = []
    return FakeFolderCollection(
        cache=json.dumps(
            asdict(
                FolderResponseInner(
                    folder_id=folder_id,
                    user_id=user_id,
                    parent_id=parent_id,
                    name=name,
                    childred_ids=choldren_ids,
                    link_ids=link_ids,
                )
            ),
            default=deep_folder_encoder,
        ),
        safe_resp=FolderResponse(
            folder_id=folder_id,
            user_id=user_id,
            parent_id=parent_id,
            name=name,
            childred_ids=choldren_ids,
            link_ids=link_ids,
        ),
        inner_resp=FolderResponseInner(
            folder_id=folder_id,
            user_id=user_id,
            parent_id=parent_id,
            name=name,
            childred_ids=choldren_ids,
            link_ids=link_ids,
        ),
        safe_del=DeletedFolderResponse(deleted_folder_id=folder_id),
        inner_del=DeletedFolderResponseInner(deleted_folder_id=folder_id),
        safe_create=CreateFolderRequest(name=name, parent_id=None),
        inner_create=CreateFolderRequestInner(
            user_id=user_id, name=name, parent_id=None
        ),
        safe_update=UpdateFolderRequest(name=name),
        inner_update=UpdateFolderRequestInner(name=name),
        safe_move=MoveFolderRequest(parent_id=parent_id),
        inner_move=MoveFolderRequestInner(parent_id=parent_id),
    )
