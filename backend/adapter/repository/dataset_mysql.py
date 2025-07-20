import json
from datetime import datetime
from typing import List, Optional
from domain import Dataset, DatasetRepository, UUID
from adapter.repository.sql import SQL, Row, Rows


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
            ) VALUES (?, ?, ?, ?, ?, ?)
        """
        # triplet_ids (List[UUID]) をJSON文字列に変換
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
        query = "SELECT * FROM datasets WHERE id = ? LIMIT 1"
        try:
            row = self.db.query_row(query, dataset_id.value)
            return self._scan_row(row)
        except Exception:
            return None

    def find_all(self) -> List[Dataset]:
        query = "SELECT * FROM datasets"
        results = []
        try:
            rows = self.db.query(query)
            while rows.next():
                result = self._scan_rows(rows)
                if result:
                    results.append(result)
            return results
        except Exception as e:
            raise RuntimeError(f"error finding all datasets: {e}")

    def update(self, dataset: Dataset) -> None:
        query = """
            UPDATE datasets SET
                name = ?,
                description = ?,
                type = ?,
                triplet_ids = ?,
                created_at = ?
            WHERE id = ?
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
        query = "DELETE FROM datasets WHERE id = ?"
        try:
            self.db.execute(query, dataset_id.value)
        except Exception as e:
            raise RuntimeError(f"error deleting dataset: {e}")

    def _scan_row(self, row: Row) -> Optional[Dataset]:
        """単一のRowからDatasetを構築するヘルパー"""
        try:
            (
                id_str,
                name,
                description,
                type,
                triplet_ids_json,
                created_at,
            ) = ("", "", "", "", "", datetime.min)
            row.scan(
                id_str,
                name,
                description,
                type,
                triplet_ids_json,
                created_at,
            )
            # JSON文字列をList[UUID]に変換
            triplet_ids = [UUID(value=tid) for tid in json.loads(triplet_ids_json)]
            return Dataset(
                ID=UUID(value=id_str),
                name=name,
                description=description,
                type=type,
                Triplet_ids=triplet_ids,
                created_at=created_at,
            )
        except Exception:
            return None

    def _scan_rows(self, rows: Rows) -> Optional[Dataset]:
        """複数のRowsからDatasetを構築するヘルパー"""
        try:
            (
                id_str,
                name,
                description,
                type,
                triplet_ids_json,
                created_at,
            ) = ("", "", "", "", "", datetime.min)
            rows.scan(
                id_str,
                name,
                description,
                type,
                triplet_ids_json,
                created_at,
            )
            triplet_ids = [UUID(value=tid) for tid in json.loads(triplet_ids_json)]
            return Dataset(
                ID=UUID(value=id_str),
                name=name,
                description=description,
                type=type,
                Triplet_ids=triplet_ids,
                created_at=created_at,
            )
        except Exception:
            return None


def NewDatasetMySQL(db: SQL) -> DatasetMySQL:
    """
    DatasetMySQLのインスタンスを生成するファクトリ関数。
    """
    return DatasetMySQL(db)