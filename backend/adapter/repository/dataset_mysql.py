import json
from datetime import datetime
from typing import List, Optional
from domain import Dataset, DatasetRepository, UUID
from adapter.repository.sql import SQL, Row, Rows, RowData


class DatasetMySQL(DatasetRepository):
    """
    DatasetRepositoryのMySQL実装。
    SQLインターフェースを介してデータベースと対話する。
    """

    def __init__(self, db: SQL):
        self.db = db

    def create(self, dataset: Dataset) -> Dataset:
        query = """
            INSERT INTO datasets (
                id, name, description, type, triplet_ids, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        triplet_ids_json = json.dumps([tid.value for tid in dataset.Triplet_ids])

        try:
            self.db.execute(
                query,
                dataset.ID.value,
                dataset.name,
                dataset.description,
                dataset.type,
                triplet_ids_json,
                dataset.created_at,
            )
            return dataset
        except Exception as e:
            raise RuntimeError(f"error creating dataset: {e}")

    def find_by_id(self, dataset_id: UUID) -> Optional[Dataset]:
        query = "SELECT * FROM datasets WHERE id = %s LIMIT 1"
        try:
            row = self.db.query_row(query, dataset_id.value)
            return self._scan_row_data(row.get_values())
        except Exception:
            return None

    def find_all(self) -> List[Dataset]:
        query = "SELECT * FROM datasets"
        results = []
        try:
            rows = self.db.query(query)
            for row_data in rows:
                result = self._scan_row_data(row_data)
                if result:
                    results.append(result)
            return results
        except Exception as e:
            raise RuntimeError(f"error finding all datasets: {e}")

    def update(self, dataset: Dataset) -> None:
        query = """
            UPDATE datasets SET
                name = %s,
                description = %s,
                type = %s,
                triplet_ids = %s,
                created_at = %s
            WHERE id = %s
        """
        triplet_ids_json = json.dumps([tid.value for tid in dataset.Triplet_ids])
        try:
            self.db.execute(
                query,
                dataset.name,
                dataset.description,
                dataset.type,
                triplet_ids_json,
                dataset.created_at,
                dataset.ID.value,
            )
        except Exception as e:
            raise RuntimeError(f"error updating dataset: {e}")

    def delete(self, dataset_id: UUID) -> None:
        query = "DELETE FROM datasets WHERE id = %s"
        try:
            self.db.execute(query, dataset_id.value)
        except Exception as e:
            raise RuntimeError(f"error deleting dataset: {e}")

    def _scan_row_data(self, row_data: Optional[RowData]) -> Optional[Dataset]:
        """単一のRowData(タプル)からDatasetを構築するヘルパー"""
        if not row_data:
            return None
        try:
            (
                id_str,
                name,
                description,
                type,
                triplet_ids_json,
                created_at,
            ) = row_data
            
            triplet_ids = [UUID(value=tid) for tid in json.loads(triplet_ids_json)]
            return Dataset(
                ID=UUID(value=id_str),
                name=name,
                description=description,
                type=type,
                Triplet_ids=triplet_ids,
                created_at=created_at,
            )
        except Exception as e:
            print(f"Error scanning row data: {e}")
            return None


def NewDatasetMySQL(db: SQL) -> DatasetMySQL:
    """
    DatasetMySQLのインスタンスを生成するファクトリ関数。
    """
    return DatasetMySQL(db)
