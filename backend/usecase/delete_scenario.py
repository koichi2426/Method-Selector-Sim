import abc
import uuid
from dataclasses import dataclass
from typing import Protocol


from domain import (
    ScenarioRepository,
)


class DeleteScenarioUseCase(Protocol):
    def execute(
        self, input_data: "DeleteScenarioInput"
    ) -> tuple["DeleteScenarioOutput", Exception | None]:
        ...


@dataclass
class DeleteScenarioInput:
    scenario_id: uuid.UUID


@dataclass
class DeleteScenarioOutput:
    ID: uuid.UUID
    message: str


class DeleteScenarioPresenter(abc.ABC):
    @abc.abstractmethod
    def output(self, deleted_id: uuid.UUID) -> DeleteScenarioOutput:
        pass


class DeleteScenarioInteractor:
    def __init__(
        self,
        presenter: DeleteScenarioPresenter,
        repo: ScenarioRepository,
        timeout_sec: int = 10,
    ):
        self.presenter = presenter
        self.repo = repo
        self.timeout_sec = timeout_sec

    def execute(
        self, input_data: DeleteScenarioInput
    ) -> tuple[DeleteScenarioOutput, Exception | None]:
        try:
            self.repo.delete(input_data.scenario_id)
            output = self.presenter.output(input_data.scenario_id)
            return output, None

        except Exception as e:
            empty_output = DeleteScenarioOutput(
                ID=input_data.scenario_id,
                message=f"Failed to delete scenario: {e}",
            )
            return empty_output, e


def new_delete_scenario_interactor(
    presenter: DeleteScenarioPresenter,
    repo: ScenarioRepository,
    timeout_sec: int,
) -> DeleteScenarioUseCase:
    return DeleteScenarioInteractor(
        presenter=presenter,
        repo=repo,
        timeout_sec=timeout_sec,
    )
