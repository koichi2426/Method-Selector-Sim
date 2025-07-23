from typing import List, Optional
from domain import TrainingReadyScenario, TrainingReadyScenarioRepository, UUID
from adapter.repository.sql import SQL, Row, Rows, RowData


class TrainingReadyScenarioMySQL(TrainingReadyScenarioRepository):
    """
    TrainingReadyScenarioRepositoryのMySQL実装。
    SQLインターフェースを介してデータベースと対話する。
    """

    def __init__(self, db: SQL):
        self.db = db

    def create(self, scenario: TrainingReadyScenario) -> TrainingReadyScenario:
        query = """
            INSERT INTO training_ready_scenarios (
                id, scenario_id, state, method_group, negative_method_group
            ) VALUES (%s, %s, %s, %s, %s)
        """
        try:
            self.db.execute(
                query,
                scenario.ID.value,
                scenario.Scenario_ID.value,
                scenario.state,
                scenario.method_group,
                scenario.negative_method_group,
            )
            return scenario
        except Exception as e:
            raise RuntimeError(f"error creating training_ready_scenario: {e}")

    def find_by_id(self, scenario_id: UUID) -> Optional[TrainingReadyScenario]:
        query = "SELECT * FROM training_ready_scenarios WHERE id = %s LIMIT 1"
        try:
            row = self.db.query_row(query, scenario_id.value)
            # 修正: _scan_row_data を使い、Rowオブジェクトから直接値を取得する
            return self._scan_row_data(row.get_values())
        except Exception:
            return None

    def find_all(self) -> List[TrainingReadyScenario]:
        query = "SELECT * FROM training_ready_scenarios"
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
            raise RuntimeError(f"error finding all training_ready_scenarios: {e}")

    def update(self, scenario: TrainingReadyScenario) -> None:
        query = """
            UPDATE training_ready_scenarios SET
                scenario_id = %s,
                state = %s,
                method_group = %s,
                negative_method_group = %s
            WHERE id = %s
        """
        try:
            self.db.execute(
                query,
                scenario.Scenario_ID.value,
                scenario.state,
                scenario.method_group,
                scenario.negative_method_group,
                scenario.ID.value,
            )
        except Exception as e:
            raise RuntimeError(f"error updating training_ready_scenario: {e}")

    def delete(self, scenario_id: UUID) -> None:
        query = "DELETE FROM training_ready_scenarios WHERE id = %s"
        try:
            self.db.execute(query, scenario_id.value)
        except Exception as e:
            raise RuntimeError(f"error deleting training_ready_scenario: {e}")

    # 修正: _scan_row / _scan_rows は RowData を直接受け取るヘルパーに統一
    def _scan_row_data(self, row_data: Optional[RowData]) -> Optional[TrainingReadyScenario]:
        """
        単一のRowData(タプル)からTrainingReadyScenarioオブジェクトを構築するヘルパー
        """
        if not row_data:
            return None
        try:
            # タプルを直接アンパックする
            (
                id_str,
                scenario_id_str,
                state,
                method_group,
                negative_method_group,
            ) = row_data
            return TrainingReadyScenario(
                ID=UUID(value=id_str),
                Scenario_ID=UUID(value=scenario_id_str),
                state=state,
                method_group=method_group,
                negative_method_group=negative_method_group,
            )
        except Exception as e:
            # エラーが発生した場合はログに出力するとデバッグしやすい
            print(f"Error scanning row data: {e}")
            return None


def NewTrainingReadyScenarioMySQL(db: SQL) -> TrainingReadyScenarioMySQL:
    """
    TrainingReadyScenarioMySQLのインスタンスを生成するファクトリ関数。
    """
    return TrainingReadyScenarioMySQL(db)