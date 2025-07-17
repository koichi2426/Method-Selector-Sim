import abc
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from .evaluation_summary import EvaluationSummary

@dataclass
class ModelEvaluationSession:
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
    def find_by_id(self, session_id: uuid.UUID) -> Optional[ModelEvaluationSession]:
        pass

    @abc.abstractmethod
    def find_all(self) -> List[ModelEvaluationSession]:
        pass

    @abc.abstractmethod
    def update(self, session: ModelEvaluationSession) -> None:
        pass

    @abc.abstractmethod
    def delete(self, session_id: uuid.UUID) -> None:
        pass

def NewModelEvaluationSession(
    ID: uuid.UUID,  # IDを引数として受け取る
    TrainedModel_ID: uuid.UUID,
    Dataset_ID: uuid.UUID,
    summary_metrics: EvaluationSummary,
    created_at: datetime,  # created_atを引数として受け取る
) -> ModelEvaluationSession:
    """
    ModelEvaluationSessionインスタンスを生成するファクトリ関数。
    """
    return ModelEvaluationSession(
        ID=ID,  # 引数で受け取ったIDを使用
        TrainedModel_ID=TrainedModel_ID,
        Dataset_ID=Dataset_ID,
        summary_metrics=summary_metrics,
        created_at=created_at,  # 引数で受け取ったcreated_atを使用
    )