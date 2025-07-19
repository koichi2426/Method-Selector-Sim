import abc
from dataclasses import dataclass
from typing import Protocol
from backend.domain import TrainingReadyScenarioRepository, UUID


class DeleteProcessedScenarioUseCase(Protocol):
    def execute(
        self, input_data: "DeleteProcessedScenarioInput"
    ) -> tuple["DeleteProcessedScenarioOutput", Exception | None]:
        ...


@dataclass
class DeleteProcessedScenarioInput:
    processed_scenario_id: UUID


@dataclass
class DeleteProcessedScenarioOutput:
    ID: UUID
    message: str


class DeleteProcessedScenarioPresenter(abc.ABC):
    @abc.abstractmethod
    def output(self, deleted_id: UUID) -> "DeleteProcessedScenarioOutput":
        pass


class DeleteProcessedScenarioInteractor:
    def __init__(
        self,
        presenter: "DeleteProcessedScenarioPresenter",
        repo: TrainingReadyScenarioRepository,
        timeout_sec: int = 10,
    ):
        self.presenter = presenter
        self.repo = repo
        self.timeout_sec = timeout_sec

    def execute(
        self, input_data: "DeleteProcessedScenarioInput"
    ) -> tuple["DeleteProcessedScenarioOutput", Exception | None]:
        try:
            self.repo.delete(input_data.processed_scenario_id)
            output = self.presenter.output(input_data.processed_scenario_id)
            return output, None

        except Exception as e:
            empty_output = DeleteProcessedScenarioOutput(
                ID=input_data.processed_scenario_id,
                message=f"Failed to delete processed scenario: {e}",
            )
            return empty_output, e


def new_delete_processed_scenario_interactor(
    presenter: "DeleteProcessedScenarioPresenter",
    repo: TrainingReadyScenarioRepository,
    timeout_sec: int,
) -> "DeleteProcessedScenarioUseCase":
    return DeleteProcessedScenarioInteractor(
        presenter=presenter,
        repo=repo,
        timeout_sec=timeout_sec,
    )
