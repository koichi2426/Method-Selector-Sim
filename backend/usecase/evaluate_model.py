import abc
from dataclasses import dataclass
from typing import Protocol
from datetime import datetime
from domain import TrainedModel, TrainedModelRepository, Dataset, DatasetRepository, ModelEvaluationSession, ModelEvaluationSessionRepository, EvaluationSummary, PerformanceEvaluatorDomainService, UUID


class EvaluateModelUseCase(Protocol):
    def execute(
        self, input_data: "EvaluateModelInput"
    ) -> tuple["EvaluateModelOutput", Exception | None]:
        ...


@dataclass
class EvaluateModelInput:
    model_id: UUID
    dataset_id: UUID


@dataclass
class EvaluationSummaryOutput:
    average_score: float
    average_inference_time_ms: float
    average_power_consumption_mw: float
    total_test_cases: int


@dataclass
class EvaluateModelOutput:
    ID: UUID
    TrainedModel_ID: UUID
    Dataset_ID: UUID
    summary_metrics: EvaluationSummaryOutput
    created_at: str


class EvaluateModelPresenter(abc.ABC):
    @abc.abstractmethod
    def output(self, session: ModelEvaluationSession) -> "EvaluateModelOutput":
        pass


class EvaluateModelInteractor:
    def __init__(
        self,
        model_repo: TrainedModelRepository,
        dataset_repo: DatasetRepository,
        session_repo: ModelEvaluationSessionRepository,
        presenter: "EvaluateModelPresenter",
        domain_service: PerformanceEvaluatorDomainService,
        timeout_sec: int = 10,
    ):
        self.model_repo = model_repo
        self.dataset_repo = dataset_repo
        self.session_repo = session_repo
        self.presenter = presenter
        self.domain_service = domain_service
        self.timeout_sec = timeout_sec

    def execute(
        self, input_data: "EvaluateModelInput"
    ) -> tuple["EvaluateModelOutput", Exception | None]:
        try:
            model = self.model_repo.find_by_id(input_data.model_id)
            if not model:
                raise ValueError(f"TrainedModel with ID {input_data.model_id} not found.")

            dataset = self.dataset_repo.find_by_id(input_data.dataset_id)
            if not dataset:
                raise ValueError(f"Dataset with ID {input_data.dataset_id} not found.")

            session = self.domain_service.evaluate_model(model, dataset)

            created_session = self.session_repo.create(session)

            output = self.presenter.output(created_session)

            return output, None

        except Exception as e:
            from domain import UUID
            empty_summary = EvaluationSummaryOutput(
                average_score=0.0,
                average_inference_time_ms=0.0,
                average_power_consumption_mw=0.0,
                total_test_cases=0,
            )
            empty_output = EvaluateModelOutput(
                ID=UUID(value="00000000-0000-0000-0000-000000000000"),
                TrainedModel_ID=input_data.model_id,
                Dataset_ID=input_data.dataset_id,
                summary_metrics=empty_summary,
                created_at=datetime.min.isoformat(),
            )
            return empty_output, e


def new_evaluate_model_interactor(
    model_repo: TrainedModelRepository,
    dataset_repo: DatasetRepository,
    session_repo: ModelEvaluationSessionRepository,
    presenter: "EvaluateModelPresenter",
    domain_service: PerformanceEvaluatorDomainService,
    timeout_sec: int,
) -> "EvaluateModelUseCase":
    return EvaluateModelInteractor(
        model_repo=model_repo,
        dataset_repo=dataset_repo,
        session_repo=session_repo,
        presenter=presenter,
        domain_service=domain_service,
        timeout_sec=timeout_sec,
    )