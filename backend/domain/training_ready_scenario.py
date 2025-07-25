import abc
from dataclasses import dataclass
from typing import List, Optional
from .custom_uuid import UUID
from datetime import datetime # datetimeをインポート

@dataclass
class TrainingReadyScenario:
    ID: UUID
    Scenario_ID: UUID
    state: str
    method_group: str
    negative_method_group: str
    created_at: datetime # created_atフィールドを追加

class TrainingReadyScenarioRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, scenario: TrainingReadyScenario) -> TrainingReadyScenario:
        pass

    @abc.abstractmethod
    def find_by_id(self, scenario_id: UUID) -> Optional[TrainingReadyScenario]:
        pass

    @abc.abstractmethod
    def find_all(self) -> List[TrainingReadyScenario]:
        pass

    @abc.abstractmethod
    def update(self, scenario: TrainingReadyScenario) -> None:
        pass

    @abc.abstractmethod
    def delete(self, scenario_id: UUID) -> None:
        pass

def NewTrainingReadyScenario(
    ID: UUID,
    Scenario_ID: UUID,
    state: str,
    method_group: str,
    negative_method_group: str,
    created_at: datetime, # created_atを引数として受け取る
) -> TrainingReadyScenario:
    return TrainingReadyScenario(
        ID=ID,
        Scenario_ID=Scenario_ID,
        state=state,
        method_group=method_group,
        negative_method_group=negative_method_group,
        created_at=created_at, # created_atを渡す
    )