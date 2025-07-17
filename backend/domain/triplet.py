import abc
import uuid
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Triplet:
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
    def find_by_id(self, triplet_id: uuid.UUID) -> Optional[Triplet]:
        pass

    @abc.abstractmethod
    def find_all(self) -> List[Triplet]:
        pass

    @abc.abstractmethod
    def update(self, triplet: Triplet) -> None:
        pass

    @abc.abstractmethod
    def delete(self, triplet_id: uuid.UUID) -> None:
        pass

def NewTriplet(
    ID: uuid.UUID,
    TrainingReadyScenario_ID: uuid.UUID,
    anchor: str,
    positive: str,
    negative: str,
) -> Triplet:
    """
    Tripletインスタンスを生成するファクトリ関数。
    """
    return Triplet(
        ID=ID,
        TrainingReadyScenario_ID=TrainingReadyScenario_ID,
        anchor=anchor,
        positive=positive,
        negative=negative,
    )