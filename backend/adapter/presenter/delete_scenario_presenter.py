from backend.usecase.delete_scenario import DeleteScenarioPresenter, DeleteScenarioOutput
from backend.domain import UUID

class DeleteScenarioPresenterImpl(DeleteScenarioPresenter):
    def output(self, deleted_id: UUID) -> DeleteScenarioOutput:
        return DeleteScenarioOutput(
            ID=deleted_id,
            message=f"Scenario {deleted_id.value} deleted successfully."
        )

def new_delete_scenario_presenter() -> DeleteScenarioPresenter:
    return DeleteScenarioPresenterImpl() 