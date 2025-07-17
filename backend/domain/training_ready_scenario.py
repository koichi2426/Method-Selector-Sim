import abc
import uuid  # uuidモジュールをインポート
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class TrainingReadyScenario:
    # IDとScenario_IDの型をstrからuuid.UUIDへ変更
    ID: uuid.UUID
    Scenario_ID: uuid.UUID
    state: str
    method_group: str
    negative_method_group: str

class TrainingReadyScenarioRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, scenario: TrainingReadyScenario) -> TrainingReadyScenario:
        pass

    @abc.abstractmethod
    def find_by_id(self, scenario_id: uuid.UUID) -> Optional[TrainingReadyScenario]: # 引数の型も変更
        pass

    @abc.abstractmethod
    def find_all(self) -> List[TrainingReadyScenario]:
        pass

    @abc.abstractmethod
    def update(self, scenario: TrainingReadyScenario) -> None:
        pass

    @abc.abstractmethod
    def delete(self, scenario_id: uuid.UUID) -> None: # 引数の型も変更
        pass