import abc
from dataclasses import dataclass
from typing import Protocol
from backend.domain import DatasetRepository, UUID


class DeleteDatasetUseCase(Protocol):
    def execute(
        self, input_data: "DeleteDatasetInput"
    ) -> tuple["DeleteDatasetOutput", Exception | None]:
        ...


@dataclass
class DeleteDatasetInput:
    dataset_id: UUID


@dataclass
class DeleteDatasetOutput:
    ID: UUID
    message: str


class DeleteDatasetPresenter(abc.ABC):
    @abc.abstractmethod
    def output(self, deleted_id: UUID) -> "DeleteDatasetOutput":
        pass


class DeleteDatasetInteractor:
    def __init__(
        self,
        presenter: "DeleteDatasetPresenter",
        repo: DatasetRepository,
        timeout_sec: int = 10,
    ):
        self.presenter = presenter
        self.repo = repo
        self.timeout_sec = timeout_sec

    def execute(
        self, input_data: "DeleteDatasetInput"
    ) -> tuple["DeleteDatasetOutput", Exception | None]:
        try:
            self.repo.delete(input_data.dataset_id)
            output = self.presenter.output(input_data.dataset_id)
            return output, None

        except Exception as e:
            empty_output = DeleteDatasetOutput(
                ID=input_data.dataset_id,
                message=f"Failed to delete dataset: {e}",
            )
            return empty_output, e


def new_delete_dataset_interactor(
    presenter: "DeleteDatasetPresenter",
    repo: DatasetRepository,
    timeout_sec: int,
) -> "DeleteDatasetUseCase":
    return DeleteDatasetInteractor(
        presenter=presenter,
        repo=repo,
        timeout_sec=timeout_sec,
    )