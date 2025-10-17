from typing import Literal, TypedDict


class Alert(TypedDict):
    level: Literal["info", "warning", "error", "critical"]
    message: str
    timestamp: str
