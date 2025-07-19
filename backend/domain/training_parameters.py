from dataclasses import dataclass

@dataclass
class TrainingParameters:
    ID: str
    name: str
    description: str
    epochs: int
    batch_size: int
    learning_rate: float

def NewTrainingParameters(
    ID: str,
    name: str,
    description: str,
    epochs: int,
    batch_size: int,
    learning_rate: float,
) -> "TrainingParameters":
    """
    TrainingParametersインスタンスを生成するファクトリ関数。
    """
    return TrainingParameters(
        ID=ID,
        name=name,
        description=description,
        epochs=epochs,
        batch_size=batch_size,
        learning_rate=learning_rate,
    )
