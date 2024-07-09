from enum import Enum
from typing import Optional

class ClassType(Enum):
    LECTURE = "Лекция"
    PRACTICE = "Практика"
    ACTIVITY = "Стадион"
    OTHER = "Другое"


class Class:
    name: Optional[str]
    type: Optional[ClassType]
    prof: Optional[str]
    url: Optional[str]
    code: Optional[str]

    def __init__(self, name: str, type: ClassType, prof: str,
                 url: Optional[str], code: Optional[str]) -> None:
        self.name = name
        self.type = type
        self.prof = prof
        self.url = url
        self.code = code



class Day:
    classes: dict[int, list[Class]] = []

    def __init__(self) -> None:
        pass