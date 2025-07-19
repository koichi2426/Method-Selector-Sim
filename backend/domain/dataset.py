import abc
from dataclasses import dataclass
from typing import List, Optional
from .custom_uuid import UUID

@dataclass
class Dataset:
    ID: UUID
    name: str
    description: str
    type: str
    Triplet_ids: List[UUID]
    created_at: str

class DatasetRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, dataset: Dataset) -> Dataset:
        pass

    @abc.abstractmethod
    def find_by_id(self, dataset_id: UUID) -> Optional[Dataset]:
        pass

    @abc.abstractmethod
    def find_all(self) -> List[Dataset]:
        pass

    @abc.abstractmethod
    def update(self, dataset: Dataset) -> None:
        pass

    @abc.abstractmethod
    def delete(self, dataset_id: UUID) -> None:
        pass

def NewDataset(
    ID: UUID,
    name: str,
    description: str,
    type: str,
    Triplet_ids: List[UUID],
    created_at: str,
) -> Dataset:
    return Dataset(
        ID=ID,
        name=name,
        description=description,
        type=type,
        Triplet_ids=Triplet_ids,
        created_at=created_at,
    )