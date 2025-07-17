from dataclasses import dataclass

@dataclass
class Situation:
    user_information: str
    environmental_information: str

def NewSituation(
    user_information: str,
    environmental_information: str,
) -> Situation:
    """
    Situationインスタンスを生成するファクトリ関数。
    """
    return Situation(
        user_information=user_information,
        environmental_information=environmental_information,
    )