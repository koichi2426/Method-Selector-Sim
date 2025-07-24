from typing import Dict, Any # DictとAnyをインポート
# from usecase.form_triplets_from import FormTripletsFromPresenter, FormTripletsFromOutput # FormTripletsFromOutput は不要になる
from usecase.form_triplets_from import FormTripletsFromPresenter
from domain import Triplet, UUID

class FormTripletsFromPresenterImpl(FormTripletsFromPresenter):
    # 返り値の型ヒントを Dict[str, Any] に変更
    def output(self, triplet: Triplet) -> Dict[str, Any]:
        """
        Tripletドメインオブジェクトを、
        JSONシリアライズ可能な辞書に変換して返す。
        """
        return {
            "ID": triplet.ID.value,                             # UUIDを文字列に変換
            "TrainingReadyScenario_ID": triplet.TrainingReadyScenario_ID.value, # UUIDを文字列に変換
            "anchor": triplet.anchor,
            "positive": triplet.positive,
            "negative": triplet.negative
        }

def new_form_triplets_from_presenter() -> FormTripletsFromPresenter:
    """
    FormTripletsFromPresenterImplのインスタンスを生成するファクトリ関数。
    """
    return FormTripletsFromPresenterImpl()