import abc
import uuid  # uuidモジュールをインポート
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Triplet:
    # IDとTrainingReadyScenario_IDの型をstrからuuid.UUIDへ変更
    ID: uuid.UUID
    TrainingReadyScenario_ID: uuid.UUID
    anchor: str
    positive: str
    negative: str

class TripletRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, triplet: Triplet) -> Triplet:
        pass

    @abc.abstractmethod
    def find_by_id(self, triplet_id: uuid.UUID) -> Optional[Triplet]: # 引数の型も変更
        pass

    @abc.abstractmethod
    def find_all(self) -> List[Triplet]:
        pass

    @abc.abstractmethod
    def update(self, triplet: Triplet) -> None:
        pass

    @abc.abstractmethod
    def delete(self, triplet_id: uuid.UUID) -> None: # 引数の型も変更
        pass