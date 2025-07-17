import abc
import uuid  # uuidモジュールをインポート
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Scenario:

    ID: uuid.UUID
    state: str
    method_group: str
    target_method: str
    negative_method_group: str

class ScenarioRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, scenario: Scenario) -> Scenario:
        pass

    @abc.abstractmethod
    def find_by_id(self, scenario_id: uuid.UUID) -> Optional[Scenario]: # 引数の型も変更
        pass

    @abc.abstractmethod
    def find_all(self) -> List[Scenario]:
        pass

    @abc.abstractmethod
    def update(self, scenario: Scenario) -> None:
        pass

    @abc.abstractmethod
    def delete(self, scenario_id: uuid.UUID) -> None: # 引数の型も変更
        pass