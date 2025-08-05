from src.auth.infrastructure.auth.password_hasher import PasswordHasher


def test_get_password_hash_success():
    password = "password"
    hashed_password = PasswordHasher.create(password)
    assert password != hashed_password
    assert type(hashed_password) is str


def test_verify_password_success():
    password = "password"
    hashed_password = PasswordHasher.create(password)
    result = PasswordHasher.verify(password, hashed_password)
    assert result is True
