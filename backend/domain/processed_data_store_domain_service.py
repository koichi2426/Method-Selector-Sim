import abc
from typing import List
from .training_ready_scenario import TrainingReadyScenario
from .custom_uuid import UUID

class ProcessedDataStoreDomainService(abc.ABC):
    @abc.abstractmethod
    def find_all_processed_scenarios(self) -> List[TrainingReadyScenario]:
        pass

    @abc.abstractmethod
    def delete_processed_scenario(self, id: UUID) -> None:
        pass