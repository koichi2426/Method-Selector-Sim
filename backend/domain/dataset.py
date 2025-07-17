import abc
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Dataset:
    ID: uuid.UUID
    name: str
    description: str
    type: str
    triplet_ids: List[uuid.UUID]
    created_at: datetime

def NewDataset(
    ID: uuid.UUID,
    name: str,
    description: str,
    type: str,
    triplet_ids: List[uuid.UUID],
    created_at: datetime
) -> Dataset:
    if not name:
        raise ValueError("Dataset name cannot be empty")
    if not type:
        raise ValueError("Dataset type cannot be empty")

    return Dataset(
        ID=ID,
        name=name,
        description=description,
        type=type,
        triplet_ids=triplet_ids,
        created_at=created_at
    )

class DatasetRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, dataset: Dataset) -> Dataset:
        pass

    @abc.abstractmethod
    def find_by_id(self, dataset_id: uuid.UUID) -> Optional[Dataset]:
        pass

    @abc.abstractmethod
    def find_all(self) -> List[Dataset]:
        pass

    @abc.abstractmethod
    def update(self, dataset: Dataset) -> None:
        pass

    @abc.abstractmethod
    def delete(self, dataset_id: uuid.UUID) -> None:
        pass