import abc
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from .evaluation_summary import EvaluationSummary

@dataclass
class ModelEvaluationSession:
    ID: str
    TrainedModel_ID: str
    Dataset_ID: str
    summary_metrics: EvaluationSummary
    created_at: datetime

class ModelEvaluationSessionRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, session: ModelEvaluationSession) -> ModelEvaluationSession:
        pass

    @abc.abstractmethod
    def find_by_id(self, session_id: str) -> Optional[ModelEvaluationSession]:
        pass

    @abc.abstractmethod
    def find_all(self) -> List[ModelEvaluationSession]:
        pass

    @abc.abstractmethod
    def update(self, session: ModelEvaluationSession) -> None:
        pass

    @abc.abstractmethod
    def delete(self, session_id: str) -> None:
        pass