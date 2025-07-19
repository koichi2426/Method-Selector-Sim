import abc
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from .custom_uuid import UUID

@dataclass
class ModelEvaluationSession:
    ID: UUID
    TrainedModel_ID: UUID
    Dataset_ID: UUID
    average_score: float
    average_inference_time_ms: float
    average_power_consumption_mw: float
    total_test_cases: int
    created_at: datetime

class ModelEvaluationSessionRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, session: ModelEvaluationSession) -> ModelEvaluationSession:
        pass

    @abc.abstractmethod
    def find_by_id(self, session_id: UUID) -> Optional[ModelEvaluationSession]:
        pass

    @abc.abstractmethod
    def find_all(self) -> List[ModelEvaluationSession]:
        pass

    @abc.abstractmethod
    def update(self, session: ModelEvaluationSession) -> None:
        pass

    @abc.abstractmethod
    def delete(self, session_id: UUID) -> None:
        pass

def NewModelEvaluationSession(
    ID: UUID,
    TrainedModel_ID: UUID,
    Dataset_ID: UUID,
    average_score: float,
    average_inference_time_ms: float,
    average_power_consumption_mw: float,
    total_test_cases: int,
    created_at: datetime,
) -> ModelEvaluationSession:
    return ModelEvaluationSession(
        ID=ID,
        TrainedModel_ID=TrainedModel_ID,
        Dataset_ID=Dataset_ID,
        average_score=average_score,
        average_inference_time_ms=average_inference_time_ms,
        average_power_consumption_mw=average_power_consumption_mw,
        total_test_cases=total_test_cases,
        created_at=created_at,
    )