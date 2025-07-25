import abc
from dataclasses import dataclass
from typing import Protocol, List
from domain import TrainingReadyScenario, TrainingReadyScenarioRepository, UUID
from datetime import datetime  # datetimeをインポート


class FindAllProcessedScenariosUseCase(Protocol):
    def execute(self) -> tuple[List["FindAllProcessedScenariosOutput"], Exception | None]:
        ...


@dataclass
class FindAllProcessedScenariosOutput:
    ID: UUID
    Scenario_ID: UUID
    state: str
    method_group: str
    negative_method_group: str
    created_at: datetime  # created_atフィールドを追加


class FindAllProcessedScenariosPresenter(abc.ABC):
    @abc.abstractmethod
    def output(self, scenarios: List[TrainingReadyScenario]) -> List["FindAllProcessedScenariosOutput"]:
        pass


class FindAllProcessedScenariosInteractor:
    def __init__(
        self,
        presenter: "FindAllProcessedScenariosPresenter",
        repo: TrainingReadyScenarioRepository,
        timeout_sec: int = 10,
    ):
        self.presenter = presenter
        self.repo = repo
        self.timeout_sec = timeout_sec

    def execute(self) -> tuple[List["FindAllProcessedScenariosOutput"], Exception | None]:
        try:
            scenarios = self.repo.find_all()
            output = self.presenter.output(scenarios)
            return output, None

        except Exception as e:
            return [], e


def new_find_all_processed_scenarios_interactor(
    presenter: "FindAllProcessedScenariosPresenter",
    repo: TrainingReadyScenarioRepository,
    timeout_sec: int,
) -> "FindAllProcessedScenariosUseCase":
    return FindAllProcessedScenariosInteractor(
        presenter=presenter,
        repo=repo,
        timeout_sec=timeout_sec,
    )