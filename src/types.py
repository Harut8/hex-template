import uuid
from typing import Union


def get_random_uuid_as_str():
    return str(uuid.uuid4())

UUID_STR = Union[uuid.UUID, str]