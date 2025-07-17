from dataclasses import dataclass
from typing import List

from .method_profile import MethodProfile
from .situation import Situation

@dataclass
class LogGenerationConfig:
    output_count: int
    method_pool: List[MethodProfile]
    situations: List[Situation]