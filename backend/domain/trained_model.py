import abc
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class TrainedModel:
    ID: uuid.UUID
    name: str
    Dataset_ID: uuid.UUID
    description: str
    file_path: str
    created_at: datetime

class TrainedModelRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, model: TrainedModel) -> TrainedModel:
        pass

    @abc.abstractmethod
    def find_by_id(self, model_id: uuid.UUID) -> Optional[TrainedModel]:
        pass

    @abc.abstractmethod
    def find_all(self) -> List[TrainedModel]:
        pass

    @abc.abstractmethod
    def update(self, model: TrainedModel) -> None:
        pass

    @abc.abstractmethod
    def delete(self, model_id: uuid.UUID) -> None:
        pass

def NewTrainedModel(
    ID: uuid.UUID,
    name: str,
    Dataset_ID: uuid.UUID,
    description: str,
    file_path: str,
    created_at: datetime,
) -> TrainedModel:
    """
    TrainedModelインスタンスを生成するファクトリ関数。
    """
    return TrainedModel(
        ID=ID,
        name=name,
        Dataset_ID=Dataset_ID,
        description=description,
        file_path=file_path,
        created_at=created_at,
    )