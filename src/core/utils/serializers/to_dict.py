from dataclasses import asdict
from typing import Any


def serialize_to_dict_exclude_none(resource: Any):
    return {key: value for key, value in asdict(resource).items() if value is not None}
