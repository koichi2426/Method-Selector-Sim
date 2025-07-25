import abc
from dataclasses import dataclass
from typing import List, Optional
from .custom_uuid import UUID
from datetime import datetime  # datetimeをインポート

@dataclass
class Triplet:
    ID: UUID
    TrainingReadyScenario_ID: UUID
    anchor: str
    positive: str
    negative: str
    created_at: datetime  # created_atフィールドを追加

class TripletRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, triplet: Triplet) -> Triplet:
        pass

    @abc.abstractmethod
    def find_by_id(self, triplet_id: UUID) -> Optional[Triplet]:
        pass

    @abc.abstractmethod
    def find_all(self) -> List[Triplet]:
        pass

    @abc.abstractmethod
    def update(self, triplet: Triplet) -> None:
        pass

    @abc.abstractmethod
    def delete(self, triplet_id: UUID) -> None:
        pass

def NewTriplet(
    ID: UUID,
    TrainingReadyScenario_ID: UUID,
    anchor: str,
    positive: str,
    negative: str,
    created_at: datetime,  # created_atを引数として受け取る
) -> Triplet:
    return Triplet(
        ID=ID,
        TrainingReadyScenario_ID=TrainingReadyScenario_ID,
        anchor=anchor,
        positive=positive,
        negative=negative,
        created_at=created_at,  # created_atを渡す
    )