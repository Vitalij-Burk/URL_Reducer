from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UpdateUserRequest(BaseModel):
    name: Optional[str] = None


class DeletedUserResponse(BaseModel):
    deleted_user_id: UUID
