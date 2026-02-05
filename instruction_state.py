from typing import TypedDict, List, Optional

class InstructionState(TypedDict, total=False):
    input: str
    intent: Optional[str]
    confidence: Optional[float]
    parsed_actions: List[dict]
    commands: List[dict]
