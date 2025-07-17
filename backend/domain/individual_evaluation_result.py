import abc
import uuid
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class IndividualEvaluationResult:
    ID: uuid.UUID
    ModelEvaluationSession_ID: uuid.UUID
    test_data_id: uuid.UUID
    inference_time_ms: float
    power_consumption_mw: float
    llm_judge_score: float
    llm_judge_reasoning: str

class IndividualEvaluationResultRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, result: IndividualEvaluationResult) -> IndividualEvaluationResult:
        pass

    @abc.abstractmethod
    def find_by_id(self, result_id: uuid.UUID) -> Optional[IndividualEvaluationResult]:
        pass

    @abc.abstractmethod
    def find_by_session_id(self, session_id: uuid.UUID) -> List[IndividualEvaluationResult]:
        pass

    @abc.abstractmethod
    def update(self, result: IndividualEvaluationResult) -> None:
        pass

    @abc.abstractmethod
    def delete(self, result_id: uuid.UUID) -> None:
        pass

def NewIndividualEvaluationResult(
    ID: uuid.UUID,  # IDを引数として受け取るように変更
    ModelEvaluationSession_ID: uuid.UUID,
    test_data_id: uuid.UUID,
    inference_time_ms: float,
    power_consumption_mw: float,
    llm_judge_score: float,
    llm_judge_reasoning: str,
) -> IndividualEvaluationResult:
    """
    IndividualEvaluationResultインスタンスを生成するファクトリ関数。
    """
    return IndividualEvaluationResult(
        ID=ID,  # 引数で受け取ったIDを使用
        ModelEvaluationSession_ID=ModelEvaluationSession_ID,
        test_data_id=test_data_id,
        inference_time_ms=inference_time_ms,
        power_consumption_mw=power_consumption_mw,
        llm_judge_score=llm_judge_score,
        llm_judge_reasoning=llm_judge_reasoning,
    )