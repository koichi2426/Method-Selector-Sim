from typing import List, Optional
from domain import Scenario, ScenarioRepository, UUID
from adapter.repository.sql import SQL, Row, Rows


class ScenarioMySQL(ScenarioRepository):
    """
    ScenarioRepositoryのMySQL実装。
    SQLインターフェースを介してデータベースと対話する。
    """

    def __init__(self, db: SQL):
        self.db = db

    def create(self, scenario: Scenario) -> Scenario:
        # 修正: プレースホルダを ? から %s に変更
        query = """
            INSERT INTO scenarios (
                id, state, method_group, target_method, negative_method_group
            ) VALUES (%s, %s, %s, %s, %s)
        """
        try:
            self.db.execute(
                query,
                scenario.ID.value,
                scenario.state,
                scenario.method_group,
                scenario.target_method,
                scenario.negative_method_group,
            )
            return scenario
        except Exception as e:
            raise RuntimeError(f"error creating scenario: {e}")

    def find_by_id(self, scenario_id: UUID) -> Optional[Scenario]:
        # 修正: プレースホルダを ? から %s に変更
        query = "SELECT * FROM scenarios WHERE id = %s LIMIT 1"
        try:
            row = self.db.query_row(query, scenario_id.value)
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
        # 修正: プレースホルダを ? から %s に変更
        query = """
            UPDATE scenarios SET
                state = %s,
                method_group = %s,
                target_method = %s,
                negative_method_group = %s
            WHERE id = %s
        """
        try:
            self.db.execute(
                query,
                scenario.state,
                scenario.method_group,
                scenario.target_method,
                scenario.negative_method_group,
                scenario.ID.value,
            )
        except Exception as e:
            raise RuntimeError(f"error updating scenario: {e}")

    def delete(self, scenario_id: UUID) -> None:
        # 修正: プレースホルダを ? から %s に変更
        query = "DELETE FROM scenarios WHERE id = %s"
        try:
            self.db.execute(query, scenario_id.value)
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
                ID=UUID(value=id_str),
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
                ID=UUID(value=id_str),
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