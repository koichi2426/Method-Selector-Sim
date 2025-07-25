from typing import List, Dict, Any
from usecase.find_all_processed_scenarios import FindAllProcessedScenariosPresenter
from domain import TrainingReadyScenario

class FindAllProcessedScenariosPresenterImpl(FindAllProcessedScenariosPresenter):
    def output(self, scenarios: List[TrainingReadyScenario]) -> List[Dict[str, Any]]:
        """
        TrainingReadyScenarioドメインオブジェクトのリストを受け取り、
        JSONシリアライズ可能な辞書のリストに変換して返す。
        """
        return [
            {
                "ID": s.ID.value,
                "Scenario_ID": s.Scenario_ID.value,
                "state": s.state,
                "method_group": [method.strip() for method in s.method_group.split(',')],
                "negative_method_group": [method.strip() for method in s.negative_method_group.split(',')],
                "created_at": s.created_at.isoformat(), # created_atを追加し、ISO形式の文字列に変換
            }
            for s in scenarios
        ]

def new_find_all_processed_scenarios_presenter() -> FindAllProcessedScenariosPresenter:
    return FindAllProcessedScenariosPresenterImpl()
