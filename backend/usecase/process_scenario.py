import abc
import uuid
from dataclasses import dataclass
from typing import Protocol

from domain import (
    Scenario,
    ScenarioRepository,
    TrainingReadyScenario,
    TrainingReadyScenarioRepository,
    PreprocessorDomainService,
)


class ProcessScenarioUseCase(Protocol):
    def execute(
        self, input_data: "ProcessScenarioInput"
    ) -> tuple["ProcessScenarioOutput", Exception | None]:
        ...


@dataclass
class ProcessScenarioInput:
    scenario_id: uuid.UUID


@dataclass
class ProcessScenarioOutput:
    ID: uuid.UUID
    Scenario_ID: uuid.UUID
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

    def execute(
        self, input_data: ProcessScenarioInput
    ) -> tuple[ProcessScenarioOutput, Exception | None]:
        try:
            scenario = self.scenario_repo.find_by_id(input_data.scenario_id)
            if not scenario:
                raise ValueError(f"Scenario with ID {input_data.scenario_id} not found.")

            training_ready_scenario = self.domain_service.process_scenario(scenario)

            created_trs = self.trs_repo.create(training_ready_scenario)

            output = self.presenter.output(created_trs)

            return output, None

        except Exception as e:
            empty_output = ProcessScenarioOutput(
                ID=uuid.UUID(int=0),
                Scenario_ID=uuid.UUID(int=0),
                state="",
                method_group="",
                negative_method_group="",
            )
            return empty_output, e


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