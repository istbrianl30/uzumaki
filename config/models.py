from dataclasses import dataclass, field
from typing import List
from datetime import datetime, timezone

@dataclass
class Card:
    id: str
    title: str
    content: str
    tags: List[str] = field(default_factory=list)
    created: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"))
    updated: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"))

    def update_timestamp(self):
        self.updated = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
