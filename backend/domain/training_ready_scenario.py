import abc
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class TrainingReadyScenario:
    ID: str
    Scenario_ID: str
    state: str
    method_group: str
    negative_method_group: str

class TrainingReadyScenarioRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, scenario: TrainingReadyScenario) -> TrainingReadyScenario:
        pass

    @abc.abstractmethod
    def find_by_id(self, scenario_id: str) -> Optional[TrainingReadyScenario]:
        pass

    @abc.abstractmethod
    def find_all(self) -> List[TrainingReadyScenario]:
        pass

    @abc.abstractmethod
    def update(self, scenario: TrainingReadyScenario) -> None:
        pass

    @abc.abstractmethod
    def delete(self, scenario_id: str) -> None:
        pass