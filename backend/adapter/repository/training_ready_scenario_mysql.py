import uuid
from typing import List, Optional

# --- 依存するインターフェースとドメインオブジェクトをインポート ---
# (実際のプロジェクト構成に合わせてパスを調整してください)
from domain.training_ready_scenario import (
    TrainingReadyScenario,
    TrainingReadyScenarioRepository,
)
from adapter.repository.sql import SQL, Row, Rows


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
            ) VALUES (?, ?, ?, ?, ?)
        """
        try:
            self.db.execute(
                query,
                str(scenario.ID),
                str(scenario.Scenario_ID),
                scenario.state,
                scenario.method_group,
                scenario.negative_method_group,
            )
            return scenario
        except Exception as e:
            raise RuntimeError(f"error creating training_ready_scenario: {e}")

    def find_by_id(self, scenario_id: uuid.UUID) -> Optional[TrainingReadyScenario]:
        query = "SELECT * FROM training_ready_scenarios WHERE id = ? LIMIT 1"
        try:
            row = self.db.query_row(query, str(scenario_id))
            return self._scan_row(row)
        except Exception:
            return None

    def find_all(self) -> List[TrainingReadyScenario]:
        query = "SELECT * FROM training_ready_scenarios"
        results = []
        try:
            rows = self.db.query(query)
            while rows.next():
                result = self._scan_rows(rows)
                if result:
                    results.append(result)
            return results
        except Exception as e:
            raise RuntimeError(f"error finding all training_ready_scenarios: {e}")

    def update(self, scenario: TrainingReadyScenario) -> None:
        query = """
            UPDATE training_ready_scenarios SET
                scenario_id = ?,
                state = ?,
                method_group = ?,
                negative_method_group = ?
            WHERE id = ?
        """
        try:
            self.db.execute(
                query,
                str(scenario.Scenario_ID),
                scenario.state,
                scenario.method_group,
                scenario.negative_method_group,
                str(scenario.ID),
            )
        except Exception as e:
            raise RuntimeError(f"error updating training_ready_scenario: {e}")

    def delete(self, scenario_id: uuid.UUID) -> None:
        query = "DELETE FROM training_ready_scenarios WHERE id = ?"
        try:
            self.db.execute(query, str(scenario_id))
        except Exception as e:
            raise RuntimeError(f"error deleting training_ready_scenario: {e}")

    def _scan_row(self, row: Row) -> Optional[TrainingReadyScenario]:
        """単一のRowからTrainingReadyScenarioを構築するヘルパー"""
        try:
            (
                id_str,
                scenario_id_str,
                state,
                method_group,
                negative_method_group,
            ) = ("", "", "", "", "")
            row.scan(
                id_str,
                scenario_id_str,
                state,
                method_group,
                negative_method_group,
            )
            return TrainingReadyScenario(
                ID=uuid.UUID(id_str),
                Scenario_ID=uuid.UUID(scenario_id_str),
                state=state,
                method_group=method_group,
                negative_method_group=negative_method_group,
            )
        except Exception:
            return None

    def _scan_rows(self, rows: Rows) -> Optional[TrainingReadyScenario]:
        """複数のRowsからTrainingReadyScenarioを構築するヘルパー"""
        try:
            (
                id_str,
                scenario_id_str,
                state,
                method_group,
                negative_method_group,
            ) = ("", "", "", "", "")
            rows.scan(
                id_str,
                scenario_id_str,
                state,
                method_group,
                negative_method_group,
            )
            return TrainingReadyScenario(
                ID=uuid.UUID(id_str),
                Scenario_ID=uuid.UUID(scenario_id_str),
                state=state,
                method_group=method_group,
                negative_method_group=negative_method_group,
            )
        except Exception:
            return None


def NewTrainingReadyScenarioMySQL(db: SQL) -> TrainingReadyScenarioMySQL:
    """
    TrainingReadyScenarioMySQLのインスタンスを生成するファクトリ関数。
    """
    return TrainingReadyScenarioMySQL(db)
