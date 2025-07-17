import abc
import uuid  # uuidモジュールをインポート
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class IndividualEvaluationResult:
    # ID関連の型をstrからuuid.UUIDへ変更
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
    def find_by_id(self, result_id: uuid.UUID) -> Optional[IndividualEvaluationResult]: # 引数の型も変更
        pass

    @abc.abstractmethod
    def find_by_session_id(self, session_id: uuid.UUID) -> List[IndividualEvaluationResult]: # 引数の型も変更
        pass

    @abc.abstractmethod
    def update(self, result: IndividualEvaluationResult) -> None:
        pass

    @abc.abstractmethod
    def delete(self, result_id: uuid.UUID) -> None: # 引数の型も変更
        pass