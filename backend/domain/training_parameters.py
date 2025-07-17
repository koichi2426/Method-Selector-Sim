from dataclasses import dataclass

@dataclass
class TrainingParameters:
    ID: str
    name: str
    description: str
    epochs: int
    batch_size: int
    learning_rate: float