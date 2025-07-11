from uuid import UUID

from pydantic import BaseModel
from pydantic import constr


class UpdateLinkRequest(BaseModel):
    name: constr(max_length=20)


class DeletedLinkResponse(BaseModel):
    deleted_link_id: UUID
