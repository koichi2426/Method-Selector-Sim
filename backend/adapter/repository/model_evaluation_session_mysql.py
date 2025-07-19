import uuid
import json
from datetime import datetime
from typing import List, Optional

# --- 依存するインターフェースとドメインオブジェクトをインポート ---
# (実際のプロジェクト構成に合わせてパスを調整してください)
from domain.model_evaluation_session import (
    ModelEvaluationSession,
    ModelEvaluationSessionRepository,
)
from domain.evaluation_summary import EvaluationSummary
from adapter.repository.sql import SQL, Row, Rows


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
            ) VALUES (?, ?, ?, ?, ?)
        """
        # summary_metrics (EvaluationSummary) をJSON文字列に変換
        summary_metrics_json = json.dumps(session.summary_metrics.__dict__)

        try:
            self.db.execute(
                query,
                str(session.ID),
                str(session.TrainedModel_ID),
                str(session.Dataset_ID),
                summary_metrics_json,
                session.created_at,
            )
            return session
        except Exception as e:
            raise RuntimeError(f"error creating model evaluation session: {e}")

    def find_by_id(self, session_id: uuid.UUID) -> Optional[ModelEvaluationSession]:
        query = "SELECT * FROM model_evaluation_sessions WHERE id = ? LIMIT 1"
        try:
            row = self.db.query_row(query, str(session_id))
            return self._scan_row(row)
        except Exception:
            return None

    def find_all(self) -> List[ModelEvaluationSession]:
        query = "SELECT * FROM model_evaluation_sessions"
        results = []
        try:
            rows = self.db.query(query)
            while rows.next():
                result = self._scan_rows(rows)
                if result:
                    results.append(result)
            return results
        except Exception as e:
            raise RuntimeError(f"error finding all model evaluation sessions: {e}")

    def update(self, session: ModelEvaluationSession) -> None:
        query = """
            UPDATE model_evaluation_sessions SET
                trained_model_id = ?,
                dataset_id = ?,
                summary_metrics = ?,
                created_at = ?
            WHERE id = ?
        """
        summary_metrics_json = json.dumps(session.summary_metrics.__dict__)
        try:
            self.db.execute(
                query,
                str(session.TrainedModel_ID),
                str(session.Dataset_ID),
                summary_metrics_json,
                session.created_at,
                str(session.ID),
            )
        except Exception as e:
            raise RuntimeError(f"error updating model evaluation session: {e}")

    def delete(self, session_id: uuid.UUID) -> None:
        query = "DELETE FROM model_evaluation_sessions WHERE id = ?"
        try:
            self.db.execute(query, str(session_id))
        except Exception as e:
            raise RuntimeError(f"error deleting model evaluation session: {e}")

    def _scan_row(self, row: Row) -> Optional[ModelEvaluationSession]:
        """単一のRowからModelEvaluationSessionを構築するヘルパー"""
        try:
            (
                id_str,
                model_id_str,
                dataset_id_str,
                summary_metrics_json,
                created_at,
            ) = ("", "", "", "{}", datetime.min)
            row.scan(
                id_str,
                model_id_str,
                dataset_id_str,
                summary_metrics_json,
                created_at,
            )
            # JSON文字列をEvaluationSummaryオブジェクトに変換
            summary_metrics = EvaluationSummary(**json.loads(summary_metrics_json))
            return ModelEvaluationSession(
                ID=uuid.UUID(id_str),
                TrainedModel_ID=uuid.UUID(model_id_str),
                Dataset_ID=uuid.UUID(dataset_id_str),
                summary_metrics=summary_metrics,
                created_at=created_at,
            )
        except Exception:
            return None

    def _scan_rows(self, rows: Rows) -> Optional[ModelEvaluationSession]:
        """複数のRowsからModelEvaluationSessionを構築するヘルパー"""
        try:
            (
                id_str,
                model_id_str,
                dataset_id_str,
                summary_metrics_json,
                created_at,
            ) = ("", "", "", "{}", datetime.min)
            rows.scan(
                id_str,
                model_id_str,
                dataset_id_str,
                summary_metrics_json,
                created_at,
            )
            summary_metrics = EvaluationSummary(**json.loads(summary_metrics_json))
            return ModelEvaluationSession(
                ID=uuid.UUID(id_str),
                TrainedModel_ID=uuid.UUID(model_id_str),
                Dataset_ID=uuid.UUID(dataset_id_str),
                summary_metrics=summary_metrics,
                created_at=created_at,
            )
        except Exception:
            return None


def NewModelEvaluationSessionMySQL(db: SQL) -> ModelEvaluationSessionMySQL:
    """
    ModelEvaluationSessionMySQLのインスタンスを生成するファクトリ関数。
    """
    return ModelEvaluationSessionMySQL(db)