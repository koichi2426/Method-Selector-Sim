import abc
from typing import List
from .triplet import Triplet
from .custom_uuid import UUID

class TripletDataStoreDomainService(abc.ABC):
    @abc.abstractmethod
    def find_all_triplets(self) -> List[Triplet]:
        pass

    @abc.abstractmethod
    def delete_triplet(self, id: UUID) -> None:
        pass