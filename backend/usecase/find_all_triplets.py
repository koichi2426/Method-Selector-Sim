import abc
from dataclasses import dataclass
from typing import Protocol, List
from domain import Triplet, TripletRepository, UUID


class FindAllTripletsUseCase(Protocol):
    def execute(self) -> tuple[List["FindAllTripletsOutput"], Exception | None]:
        ...


@dataclass
class FindAllTripletsOutput:
    ID: UUID
    TrainingReadyScenario_ID: UUID
    anchor: str
    positive: str
    negative: str


class FindAllTripletsPresenter(abc.ABC):
    @abc.abstractmethod
    def output(self, triplets: List[Triplet]) -> List["FindAllTripletsOutput"]:
        pass


class FindAllTripletsInteractor:
    def __init__(
        self,
        presenter: "FindAllTripletsPresenter",
        repo: TripletRepository,
        timeout_sec: int = 10,
    ):
        self.presenter = presenter
        self.repo = repo
        self.timeout_sec = timeout_sec

    def execute(self) -> tuple[List["FindAllTripletsOutput"], Exception | None]:
        try:
            triplets = self.repo.find_all()
            output = self.presenter.output(triplets)
            return output, None

        except Exception as e:
            return [], e


def new_find_all_triplets_interactor(
    presenter: "FindAllTripletsPresenter",
    repo: TripletRepository,
    timeout_sec: int,
) -> "FindAllTripletsUseCase":
    return FindAllTripletsInteractor(
        presenter=presenter,
        repo=repo,
        timeout_sec=timeout_sec,
    )
