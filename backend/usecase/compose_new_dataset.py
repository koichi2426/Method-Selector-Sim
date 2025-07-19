import abc
import uuid
from dataclasses import dataclass
from typing import Protocol, List
from datetime import datetime

from domain import (
    Dataset,
    DatasetRepository,
    NewDataset,
    NewUUID,
)


class ComposeNewDatasetUseCase(Protocol):
    def execute(
        self, input_data: "ComposeNewDatasetInput"
    ) -> tuple["ComposeNewDatasetOutput", Exception | None]:
        ...


@dataclass
class ComposeNewDatasetInput:
    name: str
    description: str
    triplet_ids: List[uuid.UUID]


@dataclass
class ComposeNewDatasetOutput:
    ID: uuid.UUID
    name: str
    description: str
    type: str
    Triplet_ids: List[uuid.UUID]
    created_at: str


class ComposeNewDatasetPresenter(abc.ABC):
    @abc.abstractmethod
    def output(self, dataset: Dataset) -> "ComposeNewDatasetOutput":
        pass


class ComposeNewDatasetInteractor:
    def __init__(
        self,
        dataset_repo: DatasetRepository,
        presenter: "ComposeNewDatasetPresenter",
        timeout_sec: int = 10,
    ):
        self.dataset_repo = dataset_repo
        self.presenter = presenter
        self.timeout_sec = timeout_sec

    def execute(
        self, input_data: "ComposeNewDatasetInput"
    ) -> tuple["ComposeNewDatasetOutput", Exception | None]:
        try:
            dataset = NewDataset(
                ID=NewUUID(),
                name=input_data.name,
                description=input_data.description,
                type="training",
                Triplet_ids=input_data.triplet_ids,
                created_at=datetime.now(),
            )

            created_dataset = self.dataset_repo.create(dataset)

            output = self.presenter.output(created_dataset)

            return output, None

        except Exception as e:
            empty_output = ComposeNewDatasetOutput(
                ID=uuid.UUID(int=0),
                name="",
                description="",
                type="",
                Triplet_ids=[],
                created_at=datetime.min.isoformat(),
            )
            return empty_output, e


def new_compose_new_dataset_interactor(
    dataset_repo: DatasetRepository,
    presenter: "ComposeNewDatasetPresenter",
    timeout_sec: int,
) -> "ComposeNewDatasetUseCase":
    return ComposeNewDatasetInteractor(
        dataset_repo=dataset_repo,
        presenter=presenter,
        timeout_sec=timeout_sec,
    )
