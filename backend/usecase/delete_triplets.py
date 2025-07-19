import abc
import uuid
from dataclasses import dataclass
from typing import Protocol


from domain import (
    TripletRepository,
)


class DeleteTripletsUseCase(Protocol):
    def execute(
        self, input_data: "DeleteTripletsInput"
    ) -> tuple["DeleteTripletsOutput", Exception | None]:
        ...


@dataclass
class DeleteTripletsInput:
    triplet_id: uuid.UUID


@dataclass
class DeleteTripletsOutput:
    ID: uuid.UUID
    message: str


class DeleteTripletsPresenter(abc.ABC):
    @abc.abstractmethod
    def output(self, deleted_id: uuid.UUID) -> "DeleteTripletsOutput":
        pass


class DeleteTripletsInteractor:
    def __init__(
        self,
        presenter: "DeleteTripletsPresenter",
        repo: TripletRepository,
        timeout_sec: int = 10,
    ):
        self.presenter = presenter
        self.repo = repo
        self.timeout_sec = timeout_sec

    def execute(
        self, input_data: "DeleteTripletsInput"
    ) -> tuple["DeleteTripletsOutput", Exception | None]:
        try:
            self.repo.delete(input_data.triplet_id)
            output = self.presenter.output(input_data.triplet_id)
            return output, None

        except Exception as e:
            empty_output = DeleteTripletsOutput(
                ID=input_data.triplet_id,
                message=f"Failed to delete triplet: {e}",
            )
            return empty_output, e


def new_delete_triplets_interactor(
    presenter: "DeleteTripletsPresenter",
    repo: TripletRepository,
    timeout_sec: int,
) -> "DeleteTripletsUseCase":
    return DeleteTripletsInteractor(
        presenter=presenter,
        repo=repo,
        timeout_sec=timeout_sec,
    )
