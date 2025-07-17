from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Dataset:
    ID: str
    name: str
    description: str
    type: str
    Triplet_ids: List[str]
    created_at: datetime