from src.infrastructure.auth.password_hasher import Password


def test_get_password_hash_success():
    password = "password"
    hashed_password = Password.get_password_hash(password)
    assert password != hashed_password
    assert type(hashed_password) is str


def test_verify_password_success():
    password = "password"
    hashed_password = Password.get_password_hash(password)
    result = Password.verify_password(password, hashed_password)
    assert result is True
