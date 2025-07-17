from dataclasses import dataclass
from typing import List

@dataclass
class MethodProfile:
    method_name: str
    context_keywords: List[str]