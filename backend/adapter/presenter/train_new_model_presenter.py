# from usecase.train_new_model import TrainNewModelPresenter, TrainNewModelOutput # TrainNewModelOutput は不要になる
from usecase.train_new_model import TrainNewModelPresenter
from domain import TrainedModel, UUID
from typing import Dict, Any # DictとAnyをインポート

class TrainNewModelPresenterImpl(TrainNewModelPresenter):
    # 返り値の型ヒントを Dict[str, Any] に変更
    def output(self, trained_model: TrainedModel) -> Dict[str, Any]:
        """
        TrainedModelドメインオブジェクトを、
        JSONシリアライズ可能な辞書に変換して返す。
        """
        return {
            "ID": trained_model.ID.value,                 # UUIDを文字列に変換
            "name": trained_model.name,
            "Dataset_ID": trained_model.Dataset_ID.value, # UUIDを文字列に変換
            "description": trained_model.description,
            "file_path": trained_model.file_path,
            "created_at": trained_model.created_at.isoformat() # datetimeをISO形式の文字列に変換
        }

def new_train_new_model_presenter() -> TrainNewModelPresenter:
    """
    TrainNewModelPresenterImplのインスタンスを生成するファクトリ関数。
    """
    return TrainNewModelPresenterImpl()