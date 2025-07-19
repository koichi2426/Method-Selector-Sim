from typing import List
from backend.usecase.find_all_models import FindAllModelsPresenter, FindAllModelsOutput
from backend.domain import TrainedModel, UUID

class FindAllModelsPresenterImpl(FindAllModelsPresenter):
    def output(self, models: List[TrainedModel]) -> List[FindAllModelsOutput]:
        return [FindAllModelsOutput(
            ID=m.ID,
            name=m.name,
            Dataset_ID=m.Dataset_ID,
            description=m.description,
            file_path=m.file_path,
            created_at=m.created_at.isoformat()
        ) for m in models]

def new_find_all_models_presenter() -> FindAllModelsPresenter:
    return FindAllModelsPresenterImpl() 