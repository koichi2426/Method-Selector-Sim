import abc
from dataclasses import dataclass
from typing import Protocol, List
from backend.domain import Scenario, ScenarioRepository, UUID


class FindAllScenarioUseCase(Protocol):
    def execute(self) -> tuple[List["FindAllScenarioOutput"], Exception | None]:
        ...


@dataclass
class FindAllScenarioOutput:
    ID: UUID
    state: str
    method_group: str
    target_method: str
    negative_method_group: str


class FindAllScenarioPresenter(abc.ABC):
    @abc.abstractmethod
    def output(self, scenarios: List[Scenario]) -> List[FindAllScenarioOutput]:
        pass


class FindAllScenarioInteractor:
    def __init__(
        self,
        presenter: FindAllScenarioPresenter,
        repo: ScenarioRepository,
        timeout_sec: int = 10,
    ):
        self.presenter = presenter
        self.repo = repo
        self.timeout_sec = timeout_sec

    def execute(self) -> tuple[List[FindAllScenarioOutput], Exception | None]:
        try:
            scenarios = self.repo.find_all()
            output = self.presenter.output(scenarios)
            return output, None

        except Exception as e:
            return [], e


def new_find_all_scenario_interactor(
    presenter: FindAllScenarioPresenter,
    repo: ScenarioRepository,
    timeout_sec: int,
) -> FindAllScenarioUseCase:
    return FindAllScenarioInteractor(
        presenter=presenter,
        repo=repo,
        timeout_sec=timeout_sec,
    )
