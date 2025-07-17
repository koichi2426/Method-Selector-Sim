import abc
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Scenario:
    ID: str
    state: str
    method_group: str
    target_method: str
    negative_method_group: str

class ScenarioRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, scenario: Scenario) -> Scenario:
        pass

    @abc.abstractmethod
    def find_by_id(self, scenario_id: str) -> Optional[Scenario]:
        pass

    @abc.abstractmethod
    def find_all(self) -> List[Scenario]:
        pass

    @abc.abstractmethod
    def update(self, scenario: Scenario) -> None:
        pass

    @abc.abstractmethod
    def delete(self, scenario_id: str) -> None:
        pass