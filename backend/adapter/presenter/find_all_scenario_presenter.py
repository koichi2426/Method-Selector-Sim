from typing import List
from usecase.find_all_scenario import FindAllScenarioPresenter, FindAllScenarioOutput
from domain import Scenario, UUID

class FindAllScenarioPresenterImpl(FindAllScenarioPresenter):
    def output(self, scenarios: List[Scenario]) -> List[FindAllScenarioOutput]:
        return [FindAllScenarioOutput(
            ID=s.ID,
            state=s.state,
            method_group=s.method_group,
            target_method=s.target_method,
            negative_method_group=s.negative_method_group
        ) for s in scenarios]

def new_find_all_scenario_presenter() -> FindAllScenarioPresenter:
    return FindAllScenarioPresenterImpl() 