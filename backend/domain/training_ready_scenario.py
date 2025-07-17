from dataclasses import dataclass

@dataclass
class TrainingReadyScenario:
    ID: str
    Scenario_ID: str
    state: str
    method_group: str
    negative_method_group: str