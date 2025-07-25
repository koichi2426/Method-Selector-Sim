import abc
from dataclasses import dataclass
from typing import List, Optional
from .custom_uuid import UUID
from datetime import datetime  # datetimeをインポート

@dataclass
class Scenario:
    ID: UUID
    state: str
    method_group: str
    target_method: str
    negative_method_group: str
    created_at: datetime  # created_atフィールドを追加

class ScenarioRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, scenario: Scenario) -> Scenario:
        pass

    @abc.abstractmethod
    def find_by_id(self, scenario_id: UUID) -> Optional[Scenario]:
        pass

    @abc.abstractmethod
    def find_all(self) -> List[Scenario]:
        pass

    @abc.abstractmethod
    def update(self, scenario: Scenario) -> None:
        pass

    @abc.abstractmethod
    def delete(self, scenario_id: UUID) -> None:
        pass

def NewScenario(
    ID: UUID,  # IDを引数として受け取る
    state: str,
    method_group: str,
    target_method: str,
    negative_method_group: str,
    created_at: datetime, # created_atを引数として受け取る
) -> Scenario:
    """
    Scenarioインスタンスを生成するファクトリ関数。
    """
    return Scenario(
        ID=ID,  # 引数で受け取ったIDを使用
        state=state,
        method_group=method_group,
        target_method=target_method,
        negative_method_group=negative_method_group,
        created_at=created_at, # created_atを渡す
    )