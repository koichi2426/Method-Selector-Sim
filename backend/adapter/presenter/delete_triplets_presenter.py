from typing import Dict, Any # DictとAnyをインポート
# from usecase.delete_triplets import DeleteTripletsPresenter, DeleteTripletsOutput # DeleteTripletsOutput は不要になる
from usecase.delete_triplets import DeleteTripletsPresenter
from domain import UUID

class DeleteTripletsPresenterImpl(DeleteTripletsPresenter):
    # 返り値の型ヒントを Dict[str, Any] に変更
    def output(self, deleted_id: UUID) -> Dict[str, Any]:
        """
        削除されたTripletのIDとメッセージを、
        JSONシリアライズ可能な辞書に変換して返す。
        """
        return {
            "ID": deleted_id.value, # UUIDを文字列に変換
            "message": f"Triplet {deleted_id.value} deleted successfully."
        }

def new_delete_triplets_presenter() -> DeleteTripletsPresenter:
    """
    DeleteTripletsPresenterImplのインスタンスを生成するファクトリ関数。
    """
    return DeleteTripletsPresenterImpl()