from backend.usecase.delete_model import DeleteModelPresenter, DeleteModelOutput
from backend.domain import UUID

class DeleteModelPresenterImpl(DeleteModelPresenter):
    def output(self, deleted_id: UUID) -> DeleteModelOutput:
        return DeleteModelOutput(
            ID=deleted_id,
            message=f"Model {deleted_id.value} deleted successfully."
        )

def new_delete_model_presenter() -> DeleteModelPresenter:
    return DeleteModelPresenterImpl() 