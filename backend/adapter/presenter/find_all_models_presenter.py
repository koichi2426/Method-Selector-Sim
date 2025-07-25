from typing import List, Dict, Any
from usecase.find_all_models import FindAllModelsPresenter
from domain import TrainedModel

class FindAllModelsPresenterImpl(FindAllModelsPresenter):
    def output(self, models: List[TrainedModel]) -> List[Dict[str, Any]]:
        """
        TrainedModelドメインオブジェクトのリストを受け取り、
        JSONシリアライズ可能な辞書のリストに変換して返す。
        """
        return [
            {
                "ID": m.ID.value,
                "name": m.name,
                "Dataset_ID": m.Dataset_ID.value,
                "description": m.description,
                "file_path": m.file_path,
                "created_at": m.created_at.isoformat()
            }
            for m in models
        ]

def new_find_all_models_presenter() -> FindAllModelsPresenter:
    return FindAllModelsPresenterImpl()
