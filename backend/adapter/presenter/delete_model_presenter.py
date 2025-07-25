from typing import Dict, Any # DictとAnyをインポート
# from usecase.delete_model import DeleteModelPresenter, DeleteModelOutput # DeleteModelOutput は不要になる
from usecase.delete_model import DeleteModelPresenter
from domain import UUID

class DeleteModelPresenterImpl(DeleteModelPresenter):
    # 返り値の型ヒントを Dict[str, Any] に変更
    def output(self, deleted_id: UUID) -> Dict[str, Any]:
        """
        削除されたModelのIDとメッセージを、
        JSONシリアライズ可能な辞書に変換して返す。
        """
        return {
            "ID": deleted_id.value, # UUIDを文字列に変換
            "message": f"Model {deleted_id.value} deleted successfully."
        }

def new_delete_model_presenter() -> DeleteModelPresenter:
    """
    DeleteModelPresenterImplのインスタンスを生成するファクトリ関数。
    """
    return DeleteModelPresenterImpl()