import abc
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class TrainedModel:
    ID: str
    name: str
    Dataset_ID: str
    description: str
    file_path: str
    created_at: datetime

class TrainedModelRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, model: TrainedModel) -> TrainedModel:
        pass

    @abc.abstractmethod
    def find_by_id(self, model_id: str) -> Optional[TrainedModel]:
        pass

    @abc.abstractmethod
    def find_all(self) -> List[TrainedModel]:
        pass

    @abc.abstractmethod
    def update(self, model: TrainedModel) -> None:
        pass

    @abc.abstractmethod
    def delete(self, model_id: str) -> None:
        pass