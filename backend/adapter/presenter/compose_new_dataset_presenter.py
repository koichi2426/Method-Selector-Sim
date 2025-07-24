# from usecase.compose_new_dataset import ComposeNewDatasetPresenter, ComposeNewDatasetOutput # ComposeNewDatasetOutput は不要になる可能性がある
from usecase.compose_new_dataset import ComposeNewDatasetPresenter
from domain import Dataset, UUID
from typing import Dict, Any # DictとAnyをインポート

class ComposeNewDatasetPresenterImpl(ComposeNewDatasetPresenter):
    # 返り値の型ヒントを Dict[str, Any] に変更
    def output(self, dataset: Dataset) -> Dict[str, Any]:
        """
        Datasetドメインオブジェクトを、
        JSONシリアライズ可能な辞書に変換して返す。
        """
        return {
            "ID": dataset.ID.value,                 # UUIDを文字列に変換
            "name": dataset.name,
            "description": dataset.description,
            "type": dataset.type,
            "Triplet_ids": [tid.value for tid in dataset.Triplet_ids], # UUIDのリストを文字列のリストに変換
            "created_at": dataset.created_at.isoformat() # datetimeをISO形式の文字列に変換
        }

def new_compose_new_dataset_presenter() -> ComposeNewDatasetPresenter:
    """
    ComposeNewDatasetPresenterImplのインスタンスを生成するファクトリ関数。
    """
    return ComposeNewDatasetPresenterImpl()