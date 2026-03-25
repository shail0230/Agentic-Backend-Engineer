from pydantic import BaseModel
from typing import Optional


class StepPatterns(BaseModel):
    numbered_steps: int
    bulleted_items: int
    arrow_flows: int
    has_steps: bool


class Signals(BaseModel):
    has_technical_content: bool
    has_action_items: bool
    is_structured: bool
    has_step_patterns: bool
    input_length_category: str


class PipelineOutput(BaseModel):
    word_count: int
    sentence_count: int
    keyword_frequency: dict
    technical_terms: list[str]
    action_verbs: list[str]
    sections_detected: list[str]
    step_patterns: StepPatterns
    complexity: str
    technical_density: float
    clarity_score: float
    file_processed: Optional[str] = None
    file_extracted_text_preview: Optional[str] = None
    signals: Signals
