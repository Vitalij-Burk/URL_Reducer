from src.core.utils.random.string import get_random_string


def test_get_random_string_success():
    string = get_random_string()
    assert len(string) == 8
    assert type(string) is str


def test_get_two_random_unique_strings_success():
    string1 = get_random_string()
    string2 = get_random_string()
    assert string1 != string2
