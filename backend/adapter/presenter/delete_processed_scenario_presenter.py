from typing import Dict, Any
from usecase.delete_processed_scenario import DeleteProcessedScenarioPresenter
from domain import UUID

class DeleteProcessedScenarioPresenterImpl(DeleteProcessedScenarioPresenter):
    def output(self, deleted_id: UUID) -> Dict[str, Any]:
        """
        削除されたProcessed ScenarioのIDとメッセージを、
        JSONシリアライズ可能な辞書に変換して返す。
        """
        return {
            "ID": deleted_id.value, # UUIDを文字列に変換
            "message": f"Processed scenario {deleted_id.value} deleted successfully."
        }

def new_delete_processed_scenario_presenter() -> DeleteProcessedScenarioPresenter:
    """
    DeleteProcessedScenarioPresenterImplのインスタンスを生成するファクトリ関数。
    """
    return DeleteProcessedScenarioPresenterImpl()