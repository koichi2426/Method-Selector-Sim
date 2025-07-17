import abc
import uuid  # uuidモジュールをインポート
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from .evaluation_summary import EvaluationSummary

@dataclass
class ModelEvaluationSession:
    # ID関連の型をstrからuuid.UUIDへ変更
    ID: uuid.UUID
    TrainedModel_ID: uuid.UUID
    Dataset_ID: uuid.UUID
    summary_metrics: EvaluationSummary
    created_at: datetime

class ModelEvaluationSessionRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, session: ModelEvaluationSession) -> ModelEvaluationSession:
        pass

    @abc.abstractmethod
    def find_by_id(self, session_id: uuid.UUID) -> Optional[ModelEvaluationSession]: # 引数の型も変更
        pass

    @abc.abstractmethod
    def find_all(self) -> List[ModelEvaluationSession]:
        pass

    @abc.abstractmethod
    def update(self, session: ModelEvaluationSession) -> None:
        pass

    @abc.abstractmethod
    def delete(self, session_id: uuid.UUID) -> None: # 引数の型も変更
        pass