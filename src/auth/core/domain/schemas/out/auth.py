from src.core.domain.schemas.pydantic.base import TunedModel


class AccessToken(TunedModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshToken(TunedModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenRequest(TunedModel):
    refresh_token: str
