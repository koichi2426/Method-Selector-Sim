import abc
from dataclasses import dataclass
from typing import Protocol, List
from datetime import datetime
from domain import TrainedModel, TrainedModelRepository, UUID


class FindAllModelsUseCase(Protocol):
    def execute(self) -> tuple[List["FindAllModelsOutput"], Exception | None]:
        ...


@dataclass
class FindAllModelsOutput:
    ID: UUID
    name: str
    Dataset_ID: UUID
    description: str
    file_path: str
    created_at: str


class FindAllModelsPresenter(abc.ABC):
    @abc.abstractmethod
    def output(self, models: List[TrainedModel]) -> List["FindAllModelsOutput"]:
        pass


class FindAllModelsInteractor:
    def __init__(
        self,
        presenter: "FindAllModelsPresenter",
        repo: TrainedModelRepository,
        timeout_sec: int = 10,
    ):
        self.presenter = presenter
        self.repo = repo
        self.timeout_sec = timeout_sec

    def execute(self) -> tuple[List["FindAllModelsOutput"], Exception | None]:
        try:
            models = self.repo.find_all()
            output = self.presenter.output(models)
            return output, None

        except Exception as e:
            return [], e


def new_find_all_models_interactor(
    presenter: "FindAllModelsPresenter",
    repo: TrainedModelRepository,
    timeout_sec: int,
) -> "FindAllModelsUseCase":
    return FindAllModelsInteractor(
        presenter=presenter,
        repo=repo,
        timeout_sec=timeout_sec,
    )
