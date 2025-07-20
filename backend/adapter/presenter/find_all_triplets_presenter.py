from typing import List
from usecase.find_all_triplets import FindAllTripletsPresenter, FindAllTripletsOutput
from domain import Triplet, UUID

class FindAllTripletsPresenterImpl(FindAllTripletsPresenter):
    def output(self, triplets: List[Triplet]) -> List[FindAllTripletsOutput]:
        return [FindAllTripletsOutput(
            ID=t.ID,
            TrainingReadyScenario_ID=t.TrainingReadyScenario_ID,
            anchor=t.anchor,
            positive=t.positive,
            negative=t.negative
        ) for t in triplets]

def new_find_all_triplets_presenter() -> FindAllTripletsPresenter:
    return FindAllTripletsPresenterImpl() 