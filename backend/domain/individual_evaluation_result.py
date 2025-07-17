import abc
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class IndividualEvaluationResult:
    ID: str
    ModelEvaluationSession_ID: str
    test_data_id: str
    inference_time_ms: float
    power_consumption_mw: float
    llm_judge_score: float
    llm_judge_reasoning: str

class IndividualEvaluationResultRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, result: IndividualEvaluationResult) -> IndividualEvaluationResult:
        pass

    @abc.abstractmethod
    def find_by_id(self, result_id: str) -> Optional[IndividualEvaluationResult]:
        pass

    @abc.abstractmethod
    def find_by_session_id(self, session_id: str) -> List[IndividualEvaluationResult]:
        pass

    @abc.abstractmethod
    def update(self, result: IndividualEvaluationResult) -> None:
        pass

    @abc.abstractmethod
    def delete(self, result_id: str) -> None:
        pass