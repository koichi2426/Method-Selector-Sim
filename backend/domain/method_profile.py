from dataclasses import dataclass
from typing import List

@dataclass
class MethodProfile:
    method_name: str
    context_keywords: List[str]

def NewMethodProfile(
    method_name: str,
    context_keywords: List[str],
) -> MethodProfile:
    """
    MethodProfileインスタンスを生成するファクトリ関数。
    """
    return MethodProfile(
        method_name=method_name,
        context_keywords=context_keywords,
    )