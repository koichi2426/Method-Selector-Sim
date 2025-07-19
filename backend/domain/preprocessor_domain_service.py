import abc
from typing import List
from .scenario import Scenario
from .training_ready_scenario import TrainingReadyScenario
from .custom_uuid import UUID

class PreprocessorDomainService(abc.ABC):
    @abc.abstractmethod
    def process_scenario(self, scenario: Scenario) -> TrainingReadyScenario:
        pass

    @abc.abstractmethod
    def find_all_scenario(self) -> List[Scenario]:
        pass

    @abc.abstractmethod
    def delete_scenario(self, id: UUID) -> None:
        pass
