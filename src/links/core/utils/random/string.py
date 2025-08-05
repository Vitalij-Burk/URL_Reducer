import random
import string


def get_random_string(
    length: int = 8,
    chars=string.ascii_lowercase + string.ascii_uppercase + string.digits,
) -> str:
    return "".join(random.choice(chars) for _ in range(length))
