from dataclasses import dataclass
from typing import List

from .method_profile import MethodProfile
from .situation import Situation

@dataclass
class LogGenerationConfig:
    output_count: int
    method_pool: List[MethodProfile]
    situations: List[Situation]

def NewLogGenerationConfig(
    output_count: int,
    method_pool: List[MethodProfile],
    situations: List[Situation],
) -> LogGenerationConfig:
    """
    LogGenerationConfigインスタンスを生成するファクトリ関数。
    """
    return LogGenerationConfig(
        output_count=output_count,
        method_pool=method_pool,
        situations=situations,
    )
