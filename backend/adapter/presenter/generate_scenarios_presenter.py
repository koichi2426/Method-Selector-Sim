from typing import Dict, Any
from usecase.generate_scenarios import GenerateScenariosPresenter
from domain import Scenario

class GenerateScenariosPresenterImpl(GenerateScenariosPresenter):
    def output(self, scenario: Scenario) -> Dict[str, Any]:
        """
        ドメインオブジェクトを受け取り、
        JSONシリアライズ可能な辞書に変換して返す。
        """
        return {
            "ID": scenario.ID.value,
            "state": scenario.state,
            # 文字列をカンマで分割して配列に変換
            "method_group": [method.strip() for method in scenario.method_group.split(',')],
            "target_method": scenario.target_method,
            # 文字列をカンマで分割して配列に変換
            "negative_method_group": [method.strip() for method in scenario.negative_method_group.split(',')]
        }

def new_generate_scenarios_presenter() -> GenerateScenariosPresenter:
    return GenerateScenariosPresenterImpl()
