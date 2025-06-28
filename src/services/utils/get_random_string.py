import random
import string


async def get_random_string(
    length: int = 6,
    chars=string.ascii_lowercase + string.ascii_uppercase + string.digits,
) -> str:
    return "".join(random.choice(chars) for _ in range(length))
