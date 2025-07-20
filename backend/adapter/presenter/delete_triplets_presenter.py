from usecase.delete_triplets import DeleteTripletsPresenter, DeleteTripletsOutput
from domain import UUID

class DeleteTripletsPresenterImpl(DeleteTripletsPresenter):
    def output(self, deleted_id: UUID) -> DeleteTripletsOutput:
        return DeleteTripletsOutput(
            ID=deleted_id,
            message=f"Triplet {deleted_id.value} deleted successfully."
        )

def new_delete_triplets_presenter() -> DeleteTripletsPresenter:
    return DeleteTripletsPresenterImpl() 