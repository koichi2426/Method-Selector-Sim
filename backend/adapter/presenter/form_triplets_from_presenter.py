from backend.usecase.form_triplets_from import FormTripletsFromPresenter, FormTripletsFromOutput
from backend.domain import Triplet, UUID

class FormTripletsFromPresenterImpl(FormTripletsFromPresenter):
    def output(self, triplet: Triplet) -> FormTripletsFromOutput:
        return FormTripletsFromOutput(
            ID=triplet.ID,
            TrainingReadyScenario_ID=triplet.TrainingReadyScenario_ID,
            anchor=triplet.anchor,
            positive=triplet.positive,
            negative=triplet.negative
        )

def new_form_triplets_from_presenter() -> FormTripletsFromPresenter:
    return FormTripletsFromPresenterImpl() 