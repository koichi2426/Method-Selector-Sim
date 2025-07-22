from domain.individual_evaluation_result import IndividualEvaluationResultRepository, IndividualEvaluationResult
from domain.custom_uuid import UUID
from typing import List, Optional

class IndividualEvaluationResultRepositoryImpl(IndividualEvaluationResultRepository):
    def create(self, result: IndividualEvaluationResult) -> IndividualEvaluationResult:
        raise NotImplementedError("create method is not implemented yet.")

    def find_by_id(self, result_id: UUID) -> Optional[IndividualEvaluationResult]:
        raise NotImplementedError("find_by_id method is not implemented yet.")

    def find_by_session_id(self, session_id: UUID) -> List[IndividualEvaluationResult]:
        raise NotImplementedError("find_by_session_id method is not implemented yet.")

    def find_all(self) -> List[IndividualEvaluationResult]:
        raise NotImplementedError("find_all method is not implemented yet.")

    def update(self, result: IndividualEvaluationResult) -> None:
        raise NotImplementedError("update method is not implemented yet.")

    def delete(self, result_id: UUID) -> None:
        raise NotImplementedError("delete method is not implemented yet.") 