from typing import Dict, Any
from usecase.process_scenario import ProcessScenarioPresenter
from domain import TrainingReadyScenario

class ProcessScenarioPresenterImpl(ProcessScenarioPresenter):
    def output(self, training_ready_scenario: TrainingReadyScenario) -> Dict[str, Any]:
        """
        TrainingReadyScenarioドメインオブジェクトを受け取り、
        JSONシリアライズ可能な辞書に変換して返す。
        """
        return {
            "ID": training_ready_scenario.ID.value,
            "Scenario_ID": training_ready_scenario.Scenario_ID.value,
            "state": training_ready_scenario.state,
            "method_group": [method.strip() for method in training_ready_scenario.method_group.split(',')],
            "negative_method_group": [method.strip() for method in training_ready_scenario.negative_method_group.split(',')]
        }

def new_process_scenario_presenter() -> ProcessScenarioPresenter:
    return ProcessScenarioPresenterImpl()
