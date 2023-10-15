from dataclasses import dataclass


@dataclass
class Video:
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumbnail: dict = None
    file_name: str = None
    mime_type: str = None
    file_size: int = None