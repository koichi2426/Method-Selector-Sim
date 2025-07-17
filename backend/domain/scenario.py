from dataclasses import dataclass

@dataclass
class Scenario:
    ID: str
    state: str
    method_group: str
    target_method: str
    negative_method_group: str