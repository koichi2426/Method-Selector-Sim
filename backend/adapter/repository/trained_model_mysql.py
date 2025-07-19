import uuid
from datetime import datetime
from typing import List, Optional

# --- 依存するインターフェースとドメインオブジェクトをインポート ---
# (実際のプロジェクト構成に合わせてパスを調整してください)
from domain.trained_model import TrainedModel, TrainedModelRepository
from adapter.repository.sql import SQL, Row, Rows


class TrainedModelMySQL(TrainedModelRepository):
    """
    TrainedModelRepositoryのMySQL実装。
    SQLインターフェースを介してデータベースと対話する。
    """

    def __init__(self, db: SQL):
        self.db = db

    def create(self, model: TrainedModel) -> TrainedModel:
        query = """
            INSERT INTO trained_models (
                id, name, dataset_id, description, file_path, created_at
            ) VALUES (?, ?, ?, ?, ?, ?)
        """
        try:
            self.db.execute(
                query,
                str(model.ID),
                model.name,
                str(model.Dataset_ID),
                model.description,
                model.file_path,
                model.created_at,
            )
            return model
        except Exception as e:
            raise RuntimeError(f"error creating trained model: {e}")

    def find_by_id(self, model_id: uuid.UUID) -> Optional[TrainedModel]:
        query = "SELECT * FROM trained_models WHERE id = ? LIMIT 1"
        try:
            row = self.db.query_row(query, str(model_id))
            return self._scan_row(row)
        except Exception:
            return None

    def find_all(self) -> List[TrainedModel]:
        query = "SELECT * FROM trained_models"
        results = []
        try:
            rows = self.db.query(query)
            while rows.next():
                result = self._scan_rows(rows)
                if result:
                    results.append(result)
            return results
        except Exception as e:
            raise RuntimeError(f"error finding all trained models: {e}")

    def update(self, model: TrainedModel) -> None:
        query = """
            UPDATE trained_models SET
                name = ?,
                dataset_id = ?,
                description = ?,
                file_path = ?,
                created_at = ?
            WHERE id = ?
        """
        try:
            self.db.execute(
                query,
                model.name,
                str(model.Dataset_ID),
                model.description,
                model.file_path,
                model.created_at,
                str(model.ID),
            )
        except Exception as e:
            raise RuntimeError(f"error updating trained model: {e}")

    def delete(self, model_id: uuid.UUID) -> None:
        query = "DELETE FROM trained_models WHERE id = ?"
        try:
            self.db.execute(query, str(model_id))
        except Exception as e:
            raise RuntimeError(f"error deleting trained model: {e}")

    def _scan_row(self, row: Row) -> Optional[TrainedModel]:
        """単一のRowからTrainedModelを構築するヘルパー"""
        try:
            (
                id_str,
                name,
                dataset_id_str,
                description,
                file_path,
                created_at,
            ) = ("", "", "", "", "", datetime.min)
            row.scan(
                id_str,
                name,
                dataset_id_str,
                description,
                file_path,
                created_at,
            )
            return TrainedModel(
                ID=uuid.UUID(id_str),
                name=name,
                Dataset_ID=uuid.UUID(dataset_id_str),
                description=description,
                file_path=file_path,
                created_at=created_at,
            )
        except Exception:
            return None

    def _scan_rows(self, rows: Rows) -> Optional[TrainedModel]:
        """複数のRowsからTrainedModelを構築するヘルパー"""
        try:
            (
                id_str,
                name,
                dataset_id_str,
                description,
                file_path,
                created_at,
            ) = ("", "", "", "", "", datetime.min)
            rows.scan(
                id_str,
                name,
                dataset_id_str,
                description,
                file_path,
                created_at,
            )
            return TrainedModel(
                ID=uuid.UUID(id_str),
                name=name,
                Dataset_ID=uuid.UUID(dataset_id_str),
                description=description,
                file_path=file_path,
                created_at=created_at,
            )
        except Exception:
            return None


def NewTrainedModelMySQL(db: SQL) -> TrainedModelMySQL:
    """
    TrainedModelMySQLのインスタンスを生成するファクトリ関数。
    """
    return TrainedModelMySQL(db)