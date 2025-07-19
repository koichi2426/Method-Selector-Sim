import uuid
from typing import List, Optional

# --- 依存するインターフェースとドメインオブジェクトをインポート ---
# (実際のプロジェクト構成に合わせてパスを調整してください)
from domain.triplet import (
    Triplet,
    TripletRepository,
)
from adapter.repository.sql import SQL, Row, Rows


class TripletMySQL(TripletRepository):
    """
    TripletRepositoryのMySQL実装。
    SQLインターフェースを介してデータベースと対話する。
    """

    def __init__(self, db: SQL):
        self.db = db

    def create(self, triplet: Triplet) -> Triplet:
        query = """
            INSERT INTO triplets (
                id, training_ready_scenario_id, anchor, positive, negative
            ) VALUES (?, ?, ?, ?, ?)
        """
        try:
            self.db.execute(
                query,
                str(triplet.ID),
                str(triplet.TrainingReadyScenario_ID),
                triplet.anchor,
                triplet.positive,
                triplet.negative,
            )
            return triplet
        except Exception as e:
            raise RuntimeError(f"error creating triplet: {e}")

    def find_by_id(self, triplet_id: uuid.UUID) -> Optional[Triplet]:
        query = "SELECT * FROM triplets WHERE id = ? LIMIT 1"
        try:
            row = self.db.query_row(query, str(triplet_id))
            return self._scan_row(row)
        except Exception:
            return None

    def find_all(self) -> List[Triplet]:
        query = "SELECT * FROM triplets"
        results = []
        try:
            rows = self.db.query(query)
            while rows.next():
                result = self._scan_rows(rows)
                if result:
                    results.append(result)
            return results
        except Exception as e:
            raise RuntimeError(f"error finding all triplets: {e}")

    def update(self, triplet: Triplet) -> None:
        query = """
            UPDATE triplets SET
                training_ready_scenario_id = ?,
                anchor = ?,
                positive = ?,
                negative = ?
            WHERE id = ?
        """
        try:
            self.db.execute(
                query,
                str(triplet.TrainingReadyScenario_ID),
                triplet.anchor,
                triplet.positive,
                triplet.negative,
                str(triplet.ID),
            )
        except Exception as e:
            raise RuntimeError(f"error updating triplet: {e}")

    def delete(self, triplet_id: uuid.UUID) -> None:
        query = "DELETE FROM triplets WHERE id = ?"
        try:
            self.db.execute(query, str(triplet_id))
        except Exception as e:
            raise RuntimeError(f"error deleting triplet: {e}")

    def _scan_row(self, row: Row) -> Optional[Triplet]:
        """単一のRowからTripletを構築するヘルパー"""
        try:
            (
                id_str,
                trs_id_str,
                anchor,
                positive,
                negative,
            ) = ("", "", "", "", "")
            row.scan(
                id_str,
                trs_id_str,
                anchor,
                positive,
                negative,
            )
            return Triplet(
                ID=uuid.UUID(id_str),
                TrainingReadyScenario_ID=uuid.UUID(trs_id_str),
                anchor=anchor,
                positive=positive,
                negative=negative,
            )
        except Exception:
            return None

    def _scan_rows(self, rows: Rows) -> Optional[Triplet]:
        """複数のRowsからTripletを構築するヘルパー"""
        try:
            (
                id_str,
                trs_id_str,
                anchor,
                positive,
                negative,
            ) = ("", "", "", "", "")
            rows.scan(
                id_str,
                trs_id_str,
                anchor,
                positive,
                negative,
            )
            return Triplet(
                ID=uuid.UUID(id_str),
                TrainingReadyScenario_ID=uuid.UUID(trs_id_str),
                anchor=anchor,
                positive=positive,
                negative=negative,
            )
        except Exception:
            return None


def NewTripletMySQL(db: SQL) -> TripletMySQL:
    """
    TripletMySQLのインスタンスを生成するファクトリ関数。
    """
    return TripletMySQL(db)