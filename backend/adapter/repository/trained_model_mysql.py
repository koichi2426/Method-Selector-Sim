from datetime import datetime
from typing import List, Optional
from domain import TrainedModel, TrainedModelRepository, UUID
from adapter.repository.sql import SQL, Row, Rows, RowData


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
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            self.db.execute(
                query,
                model.ID.value,
                model.name,
                model.Dataset_ID.value,
                model.description,
                model.file_path,
                model.created_at,
            )
            return model
        except Exception as e:
            raise RuntimeError(f"error creating trained model: {e}")

    def find_by_id(self, model_id: UUID) -> Optional[TrainedModel]:
        query = "SELECT * FROM trained_models WHERE id = %s LIMIT 1"
        try:
            row = self.db.query_row(query, model_id.value)
            return self._scan_row_data(row.get_values())
        except Exception:
            return None

    def find_all(self) -> List[TrainedModel]:
        query = "SELECT * FROM trained_models"
        results = []
        try:
            rows = self.db.query(query)
            for row_data in rows:
                result = self._scan_row_data(row_data)
                if result:
                    results.append(result)
            return results
        except Exception as e:
            raise RuntimeError(f"error finding all trained models: {e}")

    def update(self, model: TrainedModel) -> None:
        query = """
            UPDATE trained_models SET
                name = %s,
                dataset_id = %s,
                description = %s,
                file_path = %s,
                created_at = %s
            WHERE id = %s
        """
        try:
            self.db.execute(
                query,
                model.name,
                model.Dataset_ID.value,
                model.description,
                model.file_path,
                model.created_at,
                model.ID.value,
            )
        except Exception as e:
            raise RuntimeError(f"error updating trained model: {e}")

    def delete(self, model_id: UUID) -> None:
        query = "DELETE FROM trained_models WHERE id = %s"
        try:
            self.db.execute(query, model_id.value)
        except Exception as e:
            raise RuntimeError(f"error deleting trained model: {e}")

    def _scan_row_data(self, row_data: Optional[RowData]) -> Optional[TrainedModel]:
        """単一のRowData(タプル)からTrainedModelを構築するヘルパー"""
        if not row_data:
            return None
        try:
            (
                id_str,
                name,
                dataset_id_str,
                description,
                file_path,
                created_at,
            ) = row_data
            return TrainedModel(
                ID=UUID(value=id_str),
                name=name,
                Dataset_ID=UUID(value=dataset_id_str),
                description=description,
                file_path=file_path,
                created_at=created_at,
            )
        except Exception as e:
            print(f"Error scanning row data: {e}")
            return None


def NewTrainedModelMySQL(db: SQL) -> TrainedModelMySQL:
    """
    TrainedModelMySQLのインスタンスを生成するファクトリ関数。
    """
    return TrainedModelMySQL(db)