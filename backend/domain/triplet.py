import abc
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Triplet:
    ID: str
    TrainingReadyScenario_ID: str
    anchor: str
    positive: str
    negative: str

class TripletRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, triplet: Triplet) -> Triplet:
        pass

    @abc.abstractmethod
    def find_by_id(self, triplet_id: str) -> Optional[Triplet]:
        pass

    @abc.abstractmethod
    def find_all(self) -> List[Triplet]:
        pass

    @abc.abstractmethod
    def update(self, triplet: Triplet) -> None:
        pass

    @abc.abstractmethod
    def delete(self, triplet_id: str) -> None:
        pass