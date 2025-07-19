import uuid
from typing import List, Optional

# --- 依存するインターフェースとドメインオブジェクトをインポート ---
# (実際のプロジェクト構成に合わせてパスを調整してください)
from domain.scenario import Scenario, ScenarioRepository
from adapter.repository.sql import SQL, Row, Rows


class ScenarioMySQL(ScenarioRepository):
    """
    ScenarioRepositoryのMySQL実装。
    SQLインターフェースを介してデータベースと対話する。
    """

    def __init__(self, db: SQL):
        self.db = db

    def create(self, scenario: Scenario) -> Scenario:
        query = """
            INSERT INTO scenarios (
                id, state, method_group, target_method, negative_method_group
            ) VALUES (?, ?, ?, ?, ?)
        """
        try:
            self.db.execute(
                query,
                str(scenario.ID),
                scenario.state,
                scenario.method_group,
                scenario.target_method,
                scenario.negative_method_group,
            )
            return scenario
        except Exception as e:
            raise RuntimeError(f"error creating scenario: {e}")

    def find_by_id(self, scenario_id: uuid.UUID) -> Optional[Scenario]:
        query = "SELECT * FROM scenarios WHERE id = ? LIMIT 1"
        try:
            row = self.db.query_row(query, str(scenario_id))
            return self._scan_row(row)
        except Exception:
            # "Not Found" のような特定のエラーはここで判定し、Noneを返す
            return None

    def find_all(self) -> List[Scenario]:
        query = "SELECT * FROM scenarios"
        results = []
        try:
            rows = self.db.query(query)
            while rows.next():
                result = self._scan_rows(rows)
                if result:
                    results.append(result)
            return results
        except Exception as e:
            raise RuntimeError(f"error finding all scenarios: {e}")

    def update(self, scenario: Scenario) -> None:
        query = """
            UPDATE scenarios SET
                state = ?,
                method_group = ?,
                target_method = ?,
                negative_method_group = ?
            WHERE id = ?
        """
        try:
            self.db.execute(
                query,
                scenario.state,
                scenario.method_group,
                scenario.target_method,
                scenario.negative_method_group,
                str(scenario.ID),
            )
        except Exception as e:
            raise RuntimeError(f"error updating scenario: {e}")

    def delete(self, scenario_id: uuid.UUID) -> None:
        query = "DELETE FROM scenarios WHERE id = ?"
        try:
            self.db.execute(query, str(scenario_id))
        except Exception as e:
            raise RuntimeError(f"error deleting scenario: {e}")

    def _scan_row(self, row: Row) -> Optional[Scenario]:
        """単一のRowからScenarioを構築するヘルパー"""
        try:
            id_str, state, method_group, target_method, negative_method_group = "", "", "", "", ""
            row.scan(
                id_str,
                state,
                method_group,
                target_method,
                negative_method_group,
            )
            return Scenario(
                ID=uuid.UUID(id_str),
                state=state,
                method_group=method_group,
                target_method=target_method,
                negative_method_group=negative_method_group,
            )
        except Exception:
            return None

    def _scan_rows(self, rows: Rows) -> Optional[Scenario]:
        """複数のRowsからScenarioを構築するヘルパー"""
        try:
            id_str, state, method_group, target_method, negative_method_group = "", "", "", "", ""
            rows.scan(
                id_str,
                state,
                method_group,
                target_method,
                negative_method_group,
            )
            return Scenario(
                ID=uuid.UUID(id_str),
                state=state,
                method_group=method_group,
                target_method=target_method,
                negative_method_group=negative_method_group,
            )
        except Exception:
            return None


def NewScenarioMySQL(db: SQL) -> ScenarioMySQL:
    """
    ScenarioMySQLのインスタンスを生成するファクトリ関数。
    """
    return ScenarioMySQL(db)