from dataclasses import dataclass

@dataclass
class Triplet:
    ID: str
    TrainingReadyScenario_ID: str
    anchor: str
    positive: str
    negative: str