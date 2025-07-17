import abc
import uuid  # uuidモジュールをインポート
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Dataset:
    # IDと関連IDのリストの型を修正
    ID: uuid.UUID
    name: str
    description: str
    type: str
    Triplet_ids: List[uuid.UUID]
    created_at: datetime

class DatasetRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, dataset: Dataset) -> Dataset:
        pass

    @abc.abstractmethod
    def find_by_id(self, dataset_id: uuid.UUID) -> Optional[Dataset]: # 引数の型も変更
        pass

    @abc.abstractmethod
    def find_all(self) -> List[Dataset]:
        pass

    @abc.abstractmethod
    def update(self, dataset: Dataset) -> None:
        pass

    @abc.abstractmethod
    def delete(self, dataset_id: uuid.UUID) -> None: # 引数の型も変更
        pass