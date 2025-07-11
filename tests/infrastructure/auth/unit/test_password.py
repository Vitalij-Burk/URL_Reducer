from src.infrastructure.auth.password import Security


def test_get_password_hash_success():
    password = "password"
    hashed_password = Security.get_password_hash(password)
    assert password != hashed_password
    assert type(hashed_password) is str


def test_verify_password_success():
    password = "password"
    hashed_password = Security.get_password_hash(password)
    result = Security.verify_password(password, hashed_password)
    assert result is True
