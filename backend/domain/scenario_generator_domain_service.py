import abc
from typing import List

from .log_generation_config import LogGenerationConfig
from .scenario import Scenario

class ScenarioGeneratorDomainService(abc.ABC):
    @abc.abstractmethod
    def generate_scenarios(self, config: LogGenerationConfig) -> List[Scenario]:
        pass