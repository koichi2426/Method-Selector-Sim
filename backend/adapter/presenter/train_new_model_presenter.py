from backend.usecase.train_new_model import TrainNewModelPresenter, TrainNewModelOutput
from backend.domain import TrainedModel, UUID

class TrainNewModelPresenterImpl(TrainNewModelPresenter):
    def output(self, trained_model: TrainedModel) -> TrainNewModelOutput:
        return TrainNewModelOutput(
            ID=trained_model.ID,
            name=trained_model.name,
            Dataset_ID=trained_model.Dataset_ID,
            description=trained_model.description,
            file_path=trained_model.file_path,
            created_at=trained_model.created_at.isoformat()
        )

def new_train_new_model_presenter() -> TrainNewModelPresenter:
    return TrainNewModelPresenterImpl() 