import json
from datetime import datetime
from typing import List, Optional
from domain import ModelEvaluationSession, ModelEvaluationSessionRepository, UUID
from domain.evaluation_summary import EvaluationSummary
from adapter.repository.sql import SQL, Row, Rows, RowData


class ModelEvaluationSessionMySQL(ModelEvaluationSessionRepository):
    """
    ModelEvaluationSessionRepositoryのMySQL実装。
    SQLインターフェースを介してデータベースと対話する。
    """

    def __init__(self, db: SQL):
        self.db = db

    def create(self, session: ModelEvaluationSession) -> ModelEvaluationSession:
        query = """
            INSERT INTO model_evaluation_sessions (
                id, trained_model_id, dataset_id, summary_metrics, created_at
            ) VALUES (%s, %s, %s, %s, %s)
        """
        summary_metrics_json = json.dumps(session.summary_metrics.__dict__)

        try:
            self.db.execute(
                query,
                session.ID.value,
                session.TrainedModel_ID.value,
                session.Dataset_ID.value,
                summary_metrics_json,
                session.created_at,
            )
            return session
        except Exception as e:
            raise RuntimeError(f"error creating model evaluation session: {e}")

    def find_by_id(self, session_id: UUID) -> Optional[ModelEvaluationSession]:
        query = "SELECT * FROM model_evaluation_sessions WHERE id = %s LIMIT 1"
        try:
            row = self.db.query_row(query, session_id.value)
            return self._scan_row_data(row.get_values())
        except Exception:
            return None

    def find_all(self) -> List[ModelEvaluationSession]:
        query = "SELECT * FROM model_evaluation_sessions"
        results = []
        try:
            rows = self.db.query(query)
            for row_data in rows:
                result = self._scan_row_data(row_data)
                if result:
                    results.append(result)
            return results
        except Exception as e:
            raise RuntimeError(f"error finding all model evaluation sessions: {e}")

    def update(self, session: ModelEvaluationSession) -> None:
        query = """
            UPDATE model_evaluation_sessions SET
                trained_model_id = %s,
                dataset_id = %s,
                summary_metrics = %s,
                created_at = %s
            WHERE id = %s
        """
        summary_metrics_json = json.dumps(session.summary_metrics.__dict__)
        try:
            self.db.execute(
                query,
                session.TrainedModel_ID.value,
                session.Dataset_ID.value,
                summary_metrics_json,
                session.created_at,
                session.ID.value,
            )
        except Exception as e:
            raise RuntimeError(f"error updating model evaluation session: {e}")

    def delete(self, session_id: UUID) -> None:
        query = "DELETE FROM model_evaluation_sessions WHERE id = %s"
        try:
            self.db.execute(query, session_id.value)
        except Exception as e:
            raise RuntimeError(f"error deleting model evaluation session: {e}")

    def _scan_row_data(self, row_data: Optional[RowData]) -> Optional[ModelEvaluationSession]:
        """単一のRowData(タプル)からModelEvaluationSessionを構築するヘルパー"""
        if not row_data:
            return None
        try:
            (
                id_str,
                model_id_str,
                dataset_id_str,
                summary_metrics_json,
                created_at,
            ) = row_data
            
            summary_metrics = EvaluationSummary(**json.loads(summary_metrics_json))
            return ModelEvaluationSession(
                ID=UUID(value=id_str),
                TrainedModel_ID=UUID(value=model_id_str),
                Dataset_ID=UUID(value=dataset_id_str),
                summary_metrics=summary_metrics,
                created_at=created_at,
            )
        except Exception as e:
            print(f"Error scanning row data: {e}")
            return None


def NewModelEvaluationSessionMySQL(db: SQL) -> ModelEvaluationSessionMySQL:
    """
    ModelEvaluationSessionMySQLのインスタンスを生成するファクトリ関数。
    """
    return ModelEvaluationSessionMySQL(db)