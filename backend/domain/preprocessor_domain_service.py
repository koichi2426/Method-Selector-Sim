import abc
from typing import List
from .scenario import Scenario
from .training_ready_scenario import TrainingReadyScenario

class PreprocessorDomainService(abc.ABC):
    @abc.abstractmethod
    def process_scenario(self, scenario: Scenario) -> TrainingReadyScenario:
        pass