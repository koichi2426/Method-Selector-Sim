from typing import List, Optional
from domain import Triplet, TripletRepository, UUID
from adapter.repository.sql import SQL, RowData


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
            ) VALUES (%s, %s, %s, %s, %s)
        """
        try:
            self.db.execute(
                query,
                triplet.ID.value,
                triplet.TrainingReadyScenario_ID.value,
                triplet.anchor,
                triplet.positive,
                triplet.negative,
            )
            return triplet
        except Exception as e:
            raise RuntimeError(f"error creating triplet: {e}")

    def find_by_id(self, triplet_id: UUID) -> Optional[Triplet]:
        query = "SELECT * FROM triplets WHERE id = %s LIMIT 1"
        try:
            row = self.db.query_row(query, triplet_id.value)
            return self._scan_row_data(row.get_values())
        except Exception:
            return None

    def find_all(self) -> List[Triplet]:
        query = "SELECT * FROM triplets"
        results: List[Triplet] = []
        try:
            rows = self.db.query(query)
            for row_data in rows:
                triplet = self._scan_row_data(row_data)
                if triplet:
                    results.append(triplet)
            return results
        except Exception as e:
            raise RuntimeError(f"error finding all triplets: {e}")

    def update(self, triplet: Triplet) -> None:
        query = """
            UPDATE triplets SET
                training_ready_scenario_id = %s,
                anchor = %s,
                positive = %s,
                negative = %s
            WHERE id = %s
        """
        try:
            self.db.execute(
                query,
                triplet.TrainingReadyScenario_ID.value,
                triplet.anchor,
                triplet.positive,
                triplet.negative,
                triplet.ID.value,
            )
        except Exception as e:
            raise RuntimeError(f"error updating triplet: {e}")

    def delete(self, triplet_id: UUID) -> None:
        query = "DELETE FROM triplets WHERE id = %s"
        try:
            self.db.execute(query, triplet_id.value)
        except Exception as e:
            raise RuntimeError(f"error deleting triplet: {e}")

    def _scan_row_data(self, row_data: Optional[RowData]) -> Optional[Triplet]:
        if not row_data:
            return None
        try:
            (
                id_str,
                trs_id_str,
                anchor,
                positive,
                negative,
            ) = row_data
            return Triplet(
                ID=UUID(value=id_str),
                TrainingReadyScenario_ID=UUID(value=trs_id_str),
                anchor=anchor,
                positive=positive,
                negative=negative,
            )
        except Exception as e:
            print(f"Error scanning row data: {e}")
            return None


def NewTripletMySQL(db: SQL) -> TripletMySQL:
    """
    TripletMySQLのインスタンスを生成するファクトリ関数。
    """
    return TripletMySQL(db)
