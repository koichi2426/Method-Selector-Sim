import abc
from dataclasses import dataclass
from typing import Protocol
from backend.domain import TrainingReadyScenario, TrainingReadyScenarioRepository, Triplet, TripletRepository, TripletFormerDomainService, UUID


class FormTripletsFromUseCase(Protocol):
    def execute(
        self, input_data: "FormTripletsFromInput"
    ) -> tuple["FormTripletsFromOutput", Exception | None]:
        ...


@dataclass
class FormTripletsFromInput:
    training_ready_scenario_id: UUID


@dataclass
class FormTripletsFromOutput:
    ID: UUID
    TrainingReadyScenario_ID: UUID
    anchor: str
    positive: str
    negative: str


class FormTripletsFromPresenter(abc.ABC):
    @abc.abstractmethod
    def output(self, triplet: Triplet) -> "FormTripletsFromOutput":
        pass


class FormTripletsFromInteractor:
    def __init__(
        self,
        trs_repo: TrainingReadyScenarioRepository,
        triplet_repo: TripletRepository,
        presenter: "FormTripletsFromPresenter",
        domain_service: TripletFormerDomainService,
        timeout_sec: int = 10,
    ):
        self.trs_repo = trs_repo
        self.triplet_repo = triplet_repo
        self.presenter = presenter
        self.domain_service = domain_service
        self.timeout_sec = timeout_sec

    def execute(
        self, input_data: "FormTripletsFromInput"
    ) -> tuple["FormTripletsFromOutput", Exception | None]:
        try:
            training_ready_scenario = self.trs_repo.find_by_id(
                input_data.training_ready_scenario_id
            )
            if not training_ready_scenario:
                raise ValueError(
                    f"TrainingReadyScenario with ID {input_data.training_ready_scenario_id} not found."
                )

            triplet = self.domain_service.form_triplets_from(training_ready_scenario)

            created_triplet = self.triplet_repo.create(triplet)

            output = self.presenter.output(created_triplet)

            return output, None

        except Exception as e:
            from backend.domain import UUID
            empty_output = FormTripletsFromOutput(
                ID=UUID(value="00000000-0000-0000-0000-000000000000"),
                TrainingReadyScenario_ID=UUID(value="00000000-0000-0000-0000-000000000000"),
                anchor="",
                positive="",
                negative="",
            )
            return empty_output, e


def new_form_triplets_from_interactor(
    trs_repo: TrainingReadyScenarioRepository,
    triplet_repo: TripletRepository,
    presenter: "FormTripletsFromPresenter",
    domain_service: TripletFormerDomainService,
    timeout_sec: int,
) -> "FormTripletsFromUseCase":
    return FormTripletsFromInteractor(
        trs_repo=trs_repo,
        triplet_repo=triplet_repo,
        presenter=presenter,
        domain_service=domain_service,
        timeout_sec=timeout_sec,
    )