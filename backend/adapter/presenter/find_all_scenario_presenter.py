from typing import List, Dict, Any
from usecase.find_all_scenario import FindAllScenarioPresenter
from domain import Scenario

class FindAllScenarioPresenterImpl(FindAllScenarioPresenter):
    def output(self, scenarios: List[Scenario]) -> List[Dict[str, Any]]:
        """
        ドメインオブジェクトのリストを受け取り、
        JSONシリアライズ可能な辞書のリストに変換して返す。
        """
        
        # dataclassを介さず、直接辞書のリストを作成する
        return [
            {
                "ID": s.ID.value,
                "state": s.state,
                # 文字列をカンマで分割して配列に変換
                "method_group": [method.strip() for method in s.method_group.split(',')],
                "target_method": s.target_method,
                # 文字列をカンマで分割して配列に変換
                "negative_method_group": [method.strip() for method in s.negative_method_group.split(',')],
                "created_at": s.created_at.isoformat(), # created_atを追加し、ISO形式の文字列に変換
            }
            for s in scenarios
        ]

def new_find_all_scenario_presenter() -> FindAllScenarioPresenter:
    return FindAllScenarioPresenterImpl()
