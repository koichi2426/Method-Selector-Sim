from typing import List, Optional
from domain import IndividualEvaluationResult, IndividualEvaluationResultRepository, UUID
from adapter.repository.sql import SQL, Row, Rows, RowData


class IndividualEvaluationResultMySQL(IndividualEvaluationResultRepository):
    """
    IndividualEvaluationResultRepositoryのMySQL実装。
    SQLインターフェースを介してデータベースと対話する。
    """

    def __init__(self, db: SQL):
        self.db = db

    def create(self, result: IndividualEvaluationResult) -> IndividualEvaluationResult:
        query = """
            INSERT INTO individual_evaluation_results (
                id, model_evaluation_session_id, test_data_id, 
                inference_time_ms, power_consumption_mw, 
                llm_judge_score, llm_judge_reasoning
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        try:
            self.db.execute(
                query,
                result.ID.value,
                result.ModelEvaluationSession_ID.value,
                result.test_data_id.value,
                result.inference_time_ms,
                result.power_consumption_mw,
                result.llm_judge_score,
                result.llm_judge_reasoning,
            )
            return result
        except Exception as e:
            raise RuntimeError(f"error creating individual evaluation result: {e}")

    def find_by_id(self, result_id: UUID) -> Optional[IndividualEvaluationResult]:
        query = "SELECT * FROM individual_evaluation_results WHERE id = %s LIMIT 1"
        try:
            row = self.db.query_row(query, result_id.value)
            return self._scan_row_data(row.get_values())
        except Exception:
            return None

    def find_by_session_id(
        self, session_id: UUID
    ) -> List[IndividualEvaluationResult]:
        query = "SELECT * FROM individual_evaluation_results WHERE model_evaluation_session_id = %s"
        results = []
        try:
            rows = self.db.query(query, session_id.value)
            for row_data in rows:
                result = self._scan_row_data(row_data)
                if result:
                    results.append(result)
            return results
        except Exception as e:
            raise RuntimeError(
                f"error finding individual evaluation results by session id: {e}"
            )

    def update(self, result: IndividualEvaluationResult) -> None:
        query = """
            UPDATE individual_evaluation_results SET
                model_evaluation_session_id = %s,
                test_data_id = %s,
                inference_time_ms = %s,
                power_consumption_mw = %s,
                llm_judge_score = %s,
                llm_judge_reasoning = %s
            WHERE id = %s
        """
        try:
            self.db.execute(
                query,
                result.ModelEvaluationSession_ID.value,
                result.test_data_id.value,
                result.inference_time_ms,
                result.power_consumption_mw,
                result.llm_judge_score,
                result.llm_judge_reasoning,
                result.ID.value,
            )
        except Exception as e:
            raise RuntimeError(f"error updating individual evaluation result: {e}")

    def delete(self, result_id: UUID) -> None:
        query = "DELETE FROM individual_evaluation_results WHERE id = %s"
        try:
            self.db.execute(query, result_id.value)
        except Exception as e:
            raise RuntimeError(f"error deleting individual evaluation result: {e}")

    def _scan_row_data(self, row_data: Optional[RowData]) -> Optional[IndividualEvaluationResult]:
        """単一のRowData(タプル)からIndividualEvaluationResultを構築するヘルパー"""
        if not row_data:
            return None
        try:
            (
                id_str,
                session_id_str,
                test_data_id_str,
                inference_time,
                power_consumption,
                score,
                reasoning,
            ) = row_data

            return IndividualEvaluationResult(
                ID=UUID(value=id_str),
                ModelEvaluationSession_ID=UUID(value=session_id_str),
                test_data_id=UUID(value=test_data_id_str),
                inference_time_ms=inference_time,
                power_consumption_mw=power_consumption,
                llm_judge_score=score,
                llm_judge_reasoning=reasoning,
            )
        except Exception as e:
            print(f"Error scanning row data: {e}")
            return None


def NewIndividualEvaluationResultMySQL(db: SQL) -> IndividualEvaluationResultMySQL:
    """
    IndividualEvaluationResultMySQLのインスタンスを生成するファクトリ関数。
    """
    return IndividualEvaluationResultMySQL(db)
