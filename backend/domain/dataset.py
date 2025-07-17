import abc
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Dataset:
    ID: str
    name: str
    description: str
    type: str
    Triplet_ids: List[str]
    created_at: datetime

class DatasetRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, dataset: Dataset) -> Dataset:
        pass

    @abc.abstractmethod
    def find_by_id(self, dataset_id: str) -> Optional[Dataset]:
        pass

    @abc.abstractmethod
    def find_all(self) -> List[Dataset]:
        pass

    @abc.abstractmethod
    def update(self, dataset: Dataset) -> None:
        pass

    @abc.abstractmethod
    def delete(self, dataset_id: str) -> None:
        pass