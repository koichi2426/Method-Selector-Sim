import abc
from typing import List
from .trained_model import TrainedModel
from .custom_uuid import UUID

class ModelRegistryDomainService(abc.ABC):
    @abc.abstractmethod
    def findAllModels(self) -> List[TrainedModel]:
        pass

    @abc.abstractmethod
    def deleteModel(self, id: UUID) -> None:
        pass