from backend.usecase.generate_scenarios import GenerateScenariosPresenter, GenerateScenariosOutput
from backend.domain import Scenario, UUID

class GenerateScenariosPresenterImpl(GenerateScenariosPresenter):
    def output(self, scenario: Scenario) -> GenerateScenariosOutput:
        return GenerateScenariosOutput(
            ID=scenario.ID,
            state=scenario.state,
            method_group=scenario.method_group,
            target_method=scenario.target_method,
            negative_method_group=scenario.negative_method_group
        )

def new_generate_scenarios_presenter() -> GenerateScenariosPresenter:
    return GenerateScenariosPresenterImpl() 