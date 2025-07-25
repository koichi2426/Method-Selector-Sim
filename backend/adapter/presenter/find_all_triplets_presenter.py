from typing import List, Dict, Any # DictとAnyをインポート
# from usecase.find_all_triplets import FindAllTripletsPresenter, FindAllTripletsOutput # FindAllTripletsOutput は不要になる
from usecase.find_all_triplets import FindAllTripletsPresenter
from domain import Triplet, UUID

class FindAllTripletsPresenterImpl(FindAllTripletsPresenter):
    # 返り値の型ヒントを List[Dict[str, Any]] に変更
    def output(self, triplets: List[Triplet]) -> List[Dict[str, Any]]:
        """
        Tripletドメインオブジェクトのリストを、
        JSONシリアライズ可能な辞書のリストに変換して返す。
        """
        return [
            {
                "ID": t.ID.value,                             # UUIDを文字列に変換
                "TrainingReadyScenario_ID": t.TrainingReadyScenario_ID.value, # UUIDを文字列に変換
                "anchor": t.anchor,
                "positive": t.positive,
                "negative": t.negative,
                "created_at": t.created_at.isoformat(), # created_atを追加し、ISO形式の文字列に変換
            }
            for t in triplets
        ]

def new_find_all_triplets_presenter() -> FindAllTripletsPresenter:
    """
    FindAllTripletsPresenterImplのインスタンスを生成するファクトリ関数。
    """
    return FindAllTripletsPresenterImpl()
