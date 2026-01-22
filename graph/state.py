from typing import TypedDict, List, Dict

class ParserState(TypedDict):
    user_input: str
    actions: List[Dict]
