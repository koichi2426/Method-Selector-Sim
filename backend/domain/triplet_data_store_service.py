import abc
from typing import List

from .triplet import Triplet

class TripletDataStoreService(abc.ABC):
    @abc.abstractmethod
    def find_all_triplets(self) -> List[Triplet]:
        pass

    @abc.abstractmethod
    def delete_triplet(self, id: str) -> None:
        pass