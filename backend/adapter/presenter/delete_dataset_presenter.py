from backend.usecase.delete_dataset import DeleteDatasetPresenter, DeleteDatasetOutput
from backend.domain import UUID

class DeleteDatasetPresenterImpl(DeleteDatasetPresenter):
    def output(self, deleted_id: UUID) -> DeleteDatasetOutput:
        return DeleteDatasetOutput(
            ID=deleted_id,
            message=f"Dataset {deleted_id.value} deleted successfully."
        )

def new_delete_dataset_presenter() -> DeleteDatasetPresenter:
    return DeleteDatasetPresenterImpl() 