import abc
import uuid  # uuidモジュールをインポート
from typing import List

from .training_ready_scenario import TrainingReadyScenario

class ProcessedDataStoreDomainService(abc.ABC):
    @abc.abstractmethod
    def find_all_processed_scenarios(self) -> List[TrainingReadyScenario]:
        pass

    @abc.abstractmethod
    def delete_processed_scenario(self, id: uuid.UUID) -> None: # 引数の型も変更
        pass