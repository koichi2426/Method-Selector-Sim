from dataclasses import dataclass
from datetime import datetime

@dataclass
class TrainedModel:
    ID: str
    name: str
    Dataset_ID: str
    description: str
    file_path: str
    created_at: datetime