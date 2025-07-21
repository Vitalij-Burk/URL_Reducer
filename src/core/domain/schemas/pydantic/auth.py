from src.core.domain.schemas.pydantic.base import TunedModel


class Token(TunedModel):
    access_token: str
    token_type: str
