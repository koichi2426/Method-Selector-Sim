import abc
from dataclasses import dataclass
from typing import List, Protocol
from domain import Scenario, ScenarioRepository, MethodProfile, Situation, ScenarioGeneratorDomainService, LogGenerationConfig, UUID
from datetime import datetime  # datetimeをインポート

class GenerateScenariosUseCase(Protocol):
    def execute(
        self, input_data: "GenerateScenariosInput"
    ) -> tuple[List["GenerateScenariosOutput"], Exception | None]:
        ...


@dataclass
class GenerateScenariosInput:
    output_count: int
    method_pool: list[MethodProfile]
    situations: list[Situation]


@dataclass
class GenerateScenariosOutput:
    ID: UUID
    state: str
    method_group: str
    target_method: str
    negative_method_group: str
    created_at: datetime  # created_atフィールドを追加


class GenerateScenariosPresenter(abc.ABC):
    @abc.abstractmethod
    def output(self, scenario: Scenario) -> GenerateScenariosOutput:
        pass


class GenerateScenariosInteractor:
    def __init__(
        self,
        repo: ScenarioRepository,
        presenter: GenerateScenariosPresenter,
        domain_service: ScenarioGeneratorDomainService,
        timeout_sec: int = 10,
    ):
        self.repo = repo
        self.presenter = presenter
        self.domain_service = domain_service
        self.timeout_sec = timeout_sec

    def execute(self, input_data: GenerateScenariosInput) -> tuple[List[GenerateScenariosOutput], Exception | None]:
        try:
            config = LogGenerationConfig(
                output_count=input_data.output_count,
                method_pool=input_data.method_pool,
                situations=input_data.situations,
            )

            scenarios = self.domain_service.generate_scenarios(config)

            created_scenarios = [self.repo.create(s) for s in scenarios]

            outputs = [self.presenter.output(cs) for cs in created_scenarios]

            return outputs, None

        except Exception as e:
            return [], e


def new_generate_scenarios_interactor(
    repo: ScenarioRepository,
    presenter: GenerateScenariosPresenter,
    domain_service: ScenarioGeneratorDomainService,
    timeout_sec: int,
) -> GenerateScenariosUseCase:
    return GenerateScenariosInteractor(
        repo=repo,
        presenter=presenter,
        domain_service=domain_service,
        timeout_sec=timeout_sec,
    )