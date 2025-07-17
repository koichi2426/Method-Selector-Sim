import abc
import uuid  # uuidモジュールをインポート
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class TrainedModel:
    # ID関連の型をstrからuuid.UUIDへ変更
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
    def find_by_id(self, model_id: uuid.UUID) -> Optional[TrainedModel]: # 引数の型も変更
        pass

    @abc.abstractmethod
    def find_all(self) -> List[TrainedModel]:
        pass

    @abc.abstractmethod
    def update(self, model: TrainedModel) -> None:
        pass

    @abc.abstractmethod
    def delete(self, model_id: uuid.UUID) -> None: # 引数の型も変更
        pass