from typing import Dict, Any # DictとAnyをインポート
# from usecase.delete_dataset import DeleteDatasetPresenter, DeleteDatasetOutput # DeleteDatasetOutput は不要になる
from usecase.delete_dataset import DeleteDatasetPresenter
from domain import UUID

class DeleteDatasetPresenterImpl(DeleteDatasetPresenter):
    # 返り値の型ヒントを Dict[str, Any] に変更
    def output(self, deleted_id: UUID) -> Dict[str, Any]:
        """
        削除されたDatasetのIDとメッセージを、
        JSONシリアライズ可能な辞書に変換して返す。
        """
        return {
            "ID": deleted_id.value, # UUIDを文字列に変換
            "message": f"Dataset {deleted_id.value} deleted successfully."
        }

def new_delete_dataset_presenter() -> DeleteDatasetPresenter:
    """
    DeleteDatasetPresenterImplのインスタンスを生成するファクトリ関数。
    """
    return DeleteDatasetPresenterImpl()