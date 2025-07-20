from usecase.compose_new_dataset import ComposeNewDatasetPresenter, ComposeNewDatasetOutput
from domain import Dataset, UUID

class ComposeNewDatasetPresenterImpl(ComposeNewDatasetPresenter):
    def output(self, dataset: Dataset) -> ComposeNewDatasetOutput:
        return ComposeNewDatasetOutput(
            ID=dataset.ID,
            name=dataset.name,
            description=dataset.description,
            type=dataset.type,
            Triplet_ids=dataset.Triplet_ids,
            created_at=dataset.created_at
        )

def new_compose_new_dataset_presenter() -> ComposeNewDatasetPresenter:
    return ComposeNewDatasetPresenterImpl() 