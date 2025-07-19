import abc
from dataclasses import dataclass
from typing import List, Optional
from .custom_uuid import UUID

@dataclass
class IndividualEvaluationResult:
    ID: UUID
    ModelEvaluationSession_ID: UUID
    test_data_id: UUID
    score: float
    inference_time_ms: float
    power_consumption_mw: float

class IndividualEvaluationResultRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, result: IndividualEvaluationResult) -> IndividualEvaluationResult:
        pass

    @abc.abstractmethod
    def find_by_id(self, result_id: UUID) -> Optional[IndividualEvaluationResult]:
        pass

    @abc.abstractmethod
    def find_by_session_id(self, session_id: UUID) -> List[IndividualEvaluationResult]:
        pass

    @abc.abstractmethod
    def find_all(self) -> List[IndividualEvaluationResult]:
        pass

    @abc.abstractmethod
    def update(self, result: IndividualEvaluationResult) -> None:
        pass

    @abc.abstractmethod
    def delete(self, result_id: UUID) -> None:
        pass

def NewIndividualEvaluationResult(
    ID: UUID,
    ModelEvaluationSession_ID: UUID,
    test_data_id: UUID,
    score: float,
    inference_time_ms: float,
    power_consumption_mw: float,
) -> IndividualEvaluationResult:
    return IndividualEvaluationResult(
        ID=ID,
        ModelEvaluationSession_ID=ModelEvaluationSession_ID,
        test_data_id=test_data_id,
        score=score,
        inference_time_ms=inference_time_ms,
        power_consumption_mw=power_consumption_mw,
    )