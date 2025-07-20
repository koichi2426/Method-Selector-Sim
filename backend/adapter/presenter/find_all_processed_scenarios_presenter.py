from typing import List
from usecase.find_all_processed_scenarios import FindAllProcessedScenariosPresenter, FindAllProcessedScenariosOutput
from domain import TrainingReadyScenario, UUID

class FindAllProcessedScenariosPresenterImpl(FindAllProcessedScenariosPresenter):
    def output(self, scenarios: List[TrainingReadyScenario]) -> List[FindAllProcessedScenariosOutput]:
        return [FindAllProcessedScenariosOutput(
            ID=s.ID,
            Scenario_ID=s.Scenario_ID,
            state=s.state,
            method_group=s.method_group,
            negative_method_group=s.negative_method_group
        ) for s in scenarios]

def new_find_all_processed_scenarios_presenter() -> FindAllProcessedScenariosPresenter:
    return FindAllProcessedScenariosPresenterImpl() 