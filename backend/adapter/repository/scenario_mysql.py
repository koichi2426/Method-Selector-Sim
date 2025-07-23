from typing import List, Optional
from domain import Scenario, ScenarioRepository, UUID
from adapter.repository.sql import SQL, Row, Rows, RowData


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
        query = "SELECT * FROM scenarios WHERE id = %s LIMIT 1"
        try:
            row = self.db.query_row(query, scenario_id.value)
            # 修正: _scan_row_data を使い、Rowオブジェクトから直接値を取得する
            return self._scan_row_data(row.get_values())
        except Exception:
            return None

    def find_all(self) -> List[Scenario]:
        query = "SELECT * FROM scenarios"
        results = []
        try:
            # 修正: rowsはイテラブルなオブジェクト(データのリスト)になった
            rows = self.db.query(query)
            # 修正: 単純なforループで処理する
            for row_data in rows:
                result = self._scan_row_data(row_data)
                if result:
                    results.append(result)
            return results
        except Exception as e:
            raise RuntimeError(f"error finding all scenarios: {e}")

    def update(self, scenario: Scenario) -> None:
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
        query = "DELETE FROM scenarios WHERE id = %s"
        try:
            self.db.execute(query, scenario_id.value)
        except Exception as e:
            raise RuntimeError(f"error deleting scenario: {e}")

    # 修正: _scan_row / _scan_rows は RowData を直接受け取るヘルパーに統一
    def _scan_row_data(self, row_data: Optional[RowData]) -> Optional[Scenario]:
        """
        単一のRowData(タプル)からScenarioオブジェクトを構築するヘルパー
        """
        if not row_data:
            return None
        try:
            # タプルを直接アンパックする
            (
                id_str,
                state,
                method_group,
                target_method,
                negative_method_group,
            ) = row_data
            return Scenario(
                ID=UUID(value=id_str),
                state=state,
                method_group=method_group,
                target_method=target_method,
                negative_method_group=negative_method_group,
            )
        except Exception as e:
            # エラーが発生した場合はログに出力するとデバッグしやすい
            print(f"Error scanning row data: {e}")
            return None


def NewScenarioMySQL(db: SQL) -> ScenarioMySQL:
    """
    ScenarioMySQLのインスタンスを生成するファクトリ関数。
    """
    return ScenarioMySQL(db)
