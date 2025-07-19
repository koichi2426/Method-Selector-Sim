import abc
from dataclasses import dataclass
from typing import Protocol
from backend.domain import TrainedModelRepository, UUID


class DeleteModelUseCase(Protocol):
    def execute(
        self, input_data: "DeleteModelInput"
    ) -> tuple["DeleteModelOutput", Exception | None]:
        ...


@dataclass
class DeleteModelInput:
    model_id: UUID


@dataclass
class DeleteModelOutput:
    ID: UUID
    message: str


class DeleteModelPresenter(abc.ABC):
    @abc.abstractmethod
    def output(self, deleted_id: UUID) -> "DeleteModelOutput":
        pass


class DeleteModelInteractor:
    def __init__(
        self,
        presenter: "DeleteModelPresenter",
        repo: TrainedModelRepository,
        timeout_sec: int = 10,
    ):
        self.presenter = presenter
        self.repo = repo
        self.timeout_sec = timeout_sec

    def execute(
        self, input_data: "DeleteModelInput"
    ) -> tuple["DeleteModelOutput", Exception | None]:
        try:
            self.repo.delete(input_data.model_id)
            output = self.presenter.output(input_data.model_id)
            return output, None

        except Exception as e:
            empty_output = DeleteModelOutput(
                ID=input_data.model_id,
                message=f"Failed to delete model: {e}",
            )
            return empty_output, e


def new_delete_model_interactor(
    presenter: "DeleteModelPresenter",
    repo: TrainedModelRepository,
    timeout_sec: int,
) -> "DeleteModelUseCase":
    return DeleteModelInteractor(
        presenter=presenter,
        repo=repo,
        timeout_sec=timeout_sec,
    )
