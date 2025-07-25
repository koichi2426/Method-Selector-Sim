from typing import List, Dict, Any
from usecase.find_all_dataset import FindAllDatasetPresenter
from domain import Dataset

class FindAllDatasetPresenterImpl(FindAllDatasetPresenter):
    def output(self, datasets: List[Dataset]) -> List[Dict[str, Any]]:
        """
        Datasetドメインオブジェクトのリストを、
        JSONシリアライズ可能な辞書のリストに変換して返す。
        """
        return [
            {
                "ID": d.ID.value,
                "name": d.name,
                "description": d.description,
                "type": d.type,
                "Triplet_ids": [tid.value for tid in d.Triplet_ids],
                "created_at": d.created_at.isoformat()
            }
            for d in datasets
        ]

def new_find_all_dataset_presenter() -> FindAllDatasetPresenter:
    """
    FindAllDatasetPresenterImplのインスタンスを生成するファクトリ関数。
    """
    return FindAllDatasetPresenterImpl()
