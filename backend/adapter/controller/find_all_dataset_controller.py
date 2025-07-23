from typing import Dict, Union
from usecase.find_all_dataset import (
    FindAllDatasetUseCase,
    FindAllDatasetOutput,
)


class FindAllDatasetController:
    def __init__(self, uc: FindAllDatasetUseCase):
        self.uc = uc

    def execute(self) -> Dict[str, Union[int, FindAllDatasetOutput, Dict[str, str]]]:
        """
        Usecaseを実行し、結果を辞書形式で返す。
        """
        try:
            # Usecaseを実行して、出力とエラーを受け取る
            output, err = self.uc.execute()
            if err:
                # エラーがあれば、ステータス500とエラーメッセージを返す
                return {"status": 500, "data": {"error": str(err)}}

            # 成功すれば、ステータス200と出力データを返す
            return {"status": 200, "data": output}

        except Exception as e:
            # 予期せぬエラーが発生した場合のフォールバック
            return {"status": 500, "data": {"error": "An unexpected error occurred"}}

