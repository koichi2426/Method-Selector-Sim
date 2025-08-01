import abc
from dataclasses import dataclass
from typing import Protocol
from datetime import datetime
from domain import Dataset, DatasetRepository, TrainingParameters, NewTrainingParameters, TrainedModel, TrainedModelRepository, ModelTrainerDomainService, UUID, NewUUID


class TrainNewModelUseCase(Protocol):
    def execute(
        self, input_data: "TrainNewModelInput"
    ) -> tuple["TrainNewModelOutput", Exception | None]:
        ...


@dataclass
class TrainNewModelInput:
    dataset_id: UUID
    epochs: int
    batch_size: int
    learning_rate: float
    name: str
    description: str


@dataclass
class TrainNewModelOutput:
    ID: UUID
    name: str
    Dataset_ID: UUID
    description: str
    file_path: str
    created_at: str


class TrainNewModelPresenter(abc.ABC):
    @abc.abstractmethod
    def output(self, trained_model: TrainedModel) -> "TrainNewModelOutput":
        pass


class TrainNewModelInteractor:
    def __init__(
        self,
        dataset_repo: DatasetRepository,
        trained_model_repo: TrainedModelRepository,
        presenter: "TrainNewModelPresenter",
        domain_service: ModelTrainerDomainService,
        timeout_sec: int = 10,
    ):
        self.dataset_repo = dataset_repo
        self.trained_model_repo = trained_model_repo
        self.presenter = presenter
        self.domain_service = domain_service
        self.timeout_sec = timeout_sec

    def execute(
        self, input_data: "TrainNewModelInput"
    ) -> tuple["TrainNewModelOutput", Exception | None]:
        try:
            dataset = self.dataset_repo.find_by_id(input_data.dataset_id)
            if not dataset:
                raise ValueError(f"Dataset with ID {input_data.dataset_id} not found.")

            # NewUUID() を使用してIDを生成
            new_training_id = NewUUID()

            params = NewTrainingParameters(
                ID=new_training_id,
                name=input_data.name,
                description=input_data.description,
                epochs=input_data.epochs,
                batch_size=input_data.batch_size,
                learning_rate=input_data.learning_rate,
            )

            trained_model = self.domain_service.train_new_model(dataset, params)

            created_model = self.trained_model_repo.create(trained_model)

            output = self.presenter.output(created_model)

            return output, None

        except Exception as e:
            empty_output = TrainNewModelOutput(
                ID=UUID(value="00000000-0000-0000-0000-000000000000"),
                name="",
                Dataset_ID=UUID(value="00000000-0000-0000-0000-000000000000"),
                description="",
                file_path="",
                created_at=datetime.min.isoformat(),
            )
            return empty_output, e


def new_train_new_model_interactor(
    dataset_repo: DatasetRepository,
    trained_model_repo: TrainedModelRepository,
    presenter: "TrainNewModelPresenter",
    domain_service: ModelTrainerDomainService,
    timeout_sec: int,
) -> "TrainNewModelUseCase":
    return TrainNewModelInteractor(
        dataset_repo=dataset_repo,
        trained_model_repo=trained_model_repo,
        presenter=presenter,
        domain_service=domain_service,
        timeout_sec=timeout_sec,
    )