from typing import List, Optional
from domain import IndividualEvaluationResult, IndividualEvaluationResultRepository, UUID
from adapter.repository.sql import SQL, Row, Rows


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
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
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
            # エラーロギングなどをここで行う
            raise RuntimeError(f"error creating individual evaluation result: {e}")

    def find_by_id(self, result_id: UUID) -> Optional[IndividualEvaluationResult]:
        query = "SELECT * FROM individual_evaluation_results WHERE id = ? LIMIT 1"
        try:
            row = self.db.query_row(query, result_id.value)
            return self._scan_row(row)
        except Exception as e:
            # "Not Found" のような特定のエラーはここで判定し、Noneを返す
            # ここでは一般的なエラーとして処理
            return None

    def find_by_session_id(
        self, session_id: UUID
    ) -> List[IndividualEvaluationResult]:
        query = "SELECT * FROM individual_evaluation_results WHERE model_evaluation_session_id = ?"
        results = []
        try:
            rows = self.db.query(query, session_id.value)
            while rows.next():
                result = self._scan_rows(rows)
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
                model_evaluation_session_id = ?,
                test_data_id = ?,
                inference_time_ms = ?,
                power_consumption_mw = ?,
                llm_judge_score = ?,
                llm_judge_reasoning = ?
            WHERE id = ?
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
        query = "DELETE FROM individual_evaluation_results WHERE id = ?"
        try:
            self.db.execute(query, result_id.value)
        except Exception as e:
            raise RuntimeError(f"error deleting individual evaluation result: {e}")

    def _scan_row(self, row: Row) -> Optional[IndividualEvaluationResult]:
        """単一のRowからIndividualEvaluationResultを構築するヘルパー"""
        try:
            # プリミティブな型を格納するための変数を定義
            id_str, session_id_str, test_data_id_str = "", "", ""
            inference_time, power_consumption, score = 0.0, 0.0, 0.0
            reasoning = ""

            row.scan(
                id_str,
                session_id_str,
                test_data_id_str,
                inference_time,
                power_consumption,
                score,
                reasoning,
            )

            return IndividualEvaluationResult(
                ID=UUID(value=id_str),
                ModelEvaluationSession_ID=UUID(value=session_id_str),
                test_data_id=UUID(value=test_data_id_str),
                inference_time_ms=inference_time,
                power_consumption_mw=power_consumption,
                llm_judge_score=score,
                llm_judge_reasoning=reasoning,
            )
        except Exception:
            # Scanでエラーが発生した場合（行が存在しないなど）
            return None

    def _scan_rows(self, rows: Rows) -> Optional[IndividualEvaluationResult]:
        """複数のRowsからIndividualEvaluationResultを構築するヘルパー"""
        try:
            id_str, session_id_str, test_data_id_str = "", "", ""
            inference_time, power_consumption, score = 0.0, 0.0, 0.0
            reasoning = ""

            rows.scan(
                id_str,
                session_id_str,
                test_data_id_str,
                inference_time,
                power_consumption,
                score,
                reasoning,
            )

            return IndividualEvaluationResult(
                ID=UUID(value=id_str),
                ModelEvaluationSession_ID=UUID(value=session_id_str),
                test_data_id=UUID(value=test_data_id_str),
                inference_time_ms=inference_time,
                power_consumption_mw=power_consumption,
                llm_judge_score=score,
                llm_judge_reasoning=reasoning,
            )
        except Exception:
            return None


def NewIndividualEvaluationResultMySQL(db: SQL) -> IndividualEvaluationResultMySQL:
    """
    IndividualEvaluationResultMySQLのインスタンスを生成するファクトリ関数。
    """
    return IndividualEvaluationResultMySQL(db)