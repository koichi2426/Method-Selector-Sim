import abc
from dataclasses import dataclass
from typing import Protocol, List
from backend.domain import Scenario, ScenarioRepository, TrainingReadyScenario, TrainingReadyScenarioRepository, PreprocessorDomainService, UUID


class ProcessScenarioUseCase(Protocol):
    def execute(
        self, input_data: "ProcessScenarioInput"
    ) -> tuple[List["ProcessScenarioOutput"], Exception | None]:
        ...


@dataclass
class ProcessScenarioInput:
    scenario_ids: List[UUID]


@dataclass
class ProcessScenarioOutput:
    ID: UUID
    Scenario_ID: UUID
    state: str
    method_group: str
    negative_method_group: str


class ProcessScenarioPresenter(abc.ABC):
    @abc.abstractmethod
    def output(
        self, training_ready_scenario: TrainingReadyScenario
    ) -> ProcessScenarioOutput:
        pass


class ProcessScenarioInteractor:
    def __init__(
        self,
        scenario_repo: ScenarioRepository,
        trs_repo: TrainingReadyScenarioRepository,
        presenter: ProcessScenarioPresenter,
        domain_service: PreprocessorDomainService,
        timeout_sec: int = 10,
    ):
        self.scenario_repo = scenario_repo
        self.trs_repo = trs_repo
        self.presenter = presenter
        self.domain_service = domain_service
        self.timeout_sec = timeout_sec

    def execute(self, input_data: ProcessScenarioInput) -> tuple[List[ProcessScenarioOutput], Exception | None]:
        try:
            outputs = []
            for scenario_id in input_data.scenario_ids:
                scenario = self.scenario_repo.find_by_id(scenario_id)
                if not scenario:
                    continue

                training_ready_scenario = self.domain_service.process_scenario(scenario)

                created_trs = self.trs_repo.create(training_ready_scenario)

                output = self.presenter.output(created_trs)
                outputs.append(output)

            return outputs, None

        except Exception as e:
            return [], e


def new_process_scenario_interactor(
    scenario_repo: ScenarioRepository,
    trs_repo: TrainingReadyScenarioRepository,
    presenter: ProcessScenarioPresenter,
    domain_service: PreprocessorDomainService,
    timeout_sec: int,
) -> ProcessScenarioUseCase:
    return ProcessScenarioInteractor(
        scenario_repo=scenario_repo,
        trs_repo=trs_repo,
        presenter=presenter,
        domain_service=domain_service,
        timeout_sec=timeout_sec,
    )