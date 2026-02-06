from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import uuid

@dataclass
class NcxChapter:
    # Generate a UUID in case for some reason multiples chapter share the exact same info
    # Can also be used when looking for a specific chapter and we already know the UUID of it
    title: str
    number: int
    filepath: str
    sub_chapter: List[NcxChapter] = field(default_factory=list)
    uuid: uuid.UUID = field(default_factory=uuid.uuid4)

    def __str__(self):
        return f"{self.uuid}: {self.number} - {self.title}"

