import uuid
from dataclasses import dataclass

@dataclass
class UUID:
    value: str

def NewUUID() -> UUID:
    """新しいUUIDを生成し、UUIDオブジェクトとして返します。"""
    # uuid.uuid4()で新しいUUIDを生成し、文字列に変換してvalueにセットします
    return UUID(value=str(uuid.uuid4()))