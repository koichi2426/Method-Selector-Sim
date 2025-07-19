from backend.usecase.process_scenario import ProcessScenarioPresenter, ProcessScenarioOutput
from backend.domain import TrainingReadyScenario, UUID

class ProcessScenarioPresenterImpl(ProcessScenarioPresenter):
    def output(self, training_ready_scenario: TrainingReadyScenario) -> ProcessScenarioOutput:
        return ProcessScenarioOutput(
            ID=training_ready_scenario.ID,
            Scenario_ID=training_ready_scenario.Scenario_ID,
            state=training_ready_scenario.state,
            method_group=training_ready_scenario.method_group,
            negative_method_group=training_ready_scenario.negative_method_group
        )

def new_process_scenario_presenter() -> ProcessScenarioPresenter:
    return ProcessScenarioPresenterImpl() 