from pydantic import BaseModel
from typing import Optional

class ParsedInstruction(BaseModel):
    action: str
    browser: Optional[str] = None
    url: Optional[str] = None
    query: Optional[str] = None
    selector: Optional[str] = None
    text: Optional[str] = None
