from typing import Dict, Any
from usecase.delete_scenario import DeleteScenarioPresenter
from domain import UUID

class DeleteScenarioPresenterImpl(DeleteScenarioPresenter):
    def output(self, deleted_id: UUID) -> Dict[str, Any]:
        """
        削除されたScenarioのIDとメッセージを、
        JSONシリアライズ可能な辞書に変換して返す。
        """
        return {
            "ID": deleted_id.value, # UUIDを文字列に変換
            "message": f"Scenario {deleted_id.value} deleted successfully."
        }

def new_delete_scenario_presenter() -> DeleteScenarioPresenter:
    """
    DeleteScenarioPresenterImplのインスタンスを生成するファクトリ関数。
    """
    return DeleteScenarioPresenterImpl()