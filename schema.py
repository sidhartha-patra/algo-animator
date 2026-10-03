from typing import List, Optional, Literal, Union
from pydantic import BaseModel, Field

class Character(BaseModel):
    id: str
    name: str
    role: str = "guide"
    mood: str = "neutral"  # neutral, thinking, skeptical, explaining, confident, celebrating

class StateItem(BaseModel):
    kind: Literal["array", "variable", "pointer", "text", "graph", "bar", "water"] = "text"
    name: str
    value: str
    highlight: bool = False
    index: Optional[int] = None
    target_index: Optional[int] = None
    color: Optional[str] = None

class WhyExplanation(BaseModel):
    decision: str
    limiting_factor: str
    invariant_proof: str
    skeptical_question: str
    airtight_answer: str

class DialogueLine(BaseModel):
    character_id: str = "algo"  # "algo", "bug", "data"
    text: str
    mood: Optional[str] = "neutral"

class Scene(BaseModel):
    id: str
    type: Literal[
        "title", "intuition", "setup", "step", "decision",
        "invariant", "result", "complexity"
    ]
    title: str
    narration: str
    dialogue: List[Union[DialogueLine, str]] = Field(default_factory=list)
    states: List[StateItem] = Field(default_factory=list)
    code_line: Optional[int] = None
    duration_ms: int = 2000
    focus: Optional[str] = None
    why: Optional[WhyExplanation] = None

class AnimationSpec(BaseModel):
    title: str
    algorithm: str
    problem: str
    intuition: str
    visual_metaphor: Optional[str] = None
    invariant: str
    time_complexity: str
    space_complexity: str
    confidence: float = Field(default=1.0, ge=0, le=1)
    source_code: Optional[str] = None
    source_language: Optional[str] = "csharp"
    characters: List[Character] = Field(default_factory=list)
    scenes: List[Scene]
