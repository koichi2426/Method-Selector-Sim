from backend.usecase.delete_processed_scenario import DeleteProcessedScenarioPresenter, DeleteProcessedScenarioOutput
from backend.domain import UUID

class DeleteProcessedScenarioPresenterImpl(DeleteProcessedScenarioPresenter):
    def output(self, deleted_id: UUID) -> DeleteProcessedScenarioOutput:
        return DeleteProcessedScenarioOutput(
            ID=deleted_id,
            message=f"Processed scenario {deleted_id.value} deleted successfully."
        )

def new_delete_processed_scenario_presenter() -> DeleteProcessedScenarioPresenter:
    return DeleteProcessedScenarioPresenterImpl() 