from dataclasses import dataclass


@dataclass
class TokenInner:
    access_token: str
    token_type: str
